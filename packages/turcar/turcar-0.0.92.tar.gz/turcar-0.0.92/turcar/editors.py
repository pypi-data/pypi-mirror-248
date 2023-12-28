# -*- coding: utf-8 -*-
import base64
import datetime
import hashlib
import json
import os.path
import re
import os
import sys
import time
import tkinter as tk
import platform
import traceback
import urllib
from logging import exception, getLogger
from tkinter import messagebox, simpledialog, ttk
from typing import Optional, Union
# import cv2
import requests
from _tkinter import TclError
from turcar import get_runner, get_workbench, ui_utils
from turcar.base_file_browser import ask_backend_path, choose_node_for_file_operations
from turcar.codeview import BinaryFileException, CodeView, CodeViewText
from tkinter import ttk
from turcar.common import (
    REMOTE_PATH_MARKER,
    InlineCommand,
    TextRange,
    ToplevelResponse,
    is_local_path,
    is_remote_path,
    is_same_path,
    normpath_with_actual_case,
    universal_dirname,
)
from turcar.custom_notebook import CustomNotebook, CustomNotebookTab
from turcar.languages import tr
from turcar.misc_utils import running_on_mac_os, running_on_windows
from turcar.tktextext import rebind_control_a
from turcar.ui_utils import (
    askopenfilename,
    asksaveasfilename,
    get_beam_cursor,
    select_sequence,
    windows_known_extensions_are_hidden,
)
from turcar.video import VideoDialog

PYTHON_FILES_STR = tr("Python files")
_dialog_filetypes = [(PYTHON_FILES_STR, ".py .pyw .pyi"), (tr("all files"), ".*")]

PYTHON_EXTENSIONS = {"py", "pyw", "pyi"}
PYTHONLIKE_EXTENSIONS = set()

logger = getLogger(__name__)


class EditorCodeViewText(CodeViewText):
    """Allows separate class binding for CodeViewTexts which are inside editors"""

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(
            master=master,
            cnf=cnf,
            **kw,
        )
        self.bindtags(self.bindtags() + ("EditorCodeViewText",))


class Editor(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        assert isinstance(master, EditorNotebook)
        self.containing_notebook = master  # type: EditorNotebook

        self._code_view = CodeView(
            self,
            propose_remove_line_numbers=True,
            font="EditorFont",
            text_class=EditorCodeViewText,
            cursor=get_beam_cursor(),
        )
        get_workbench().event_generate(
            "EditorTextCreated", editor=self, text_widget=self.get_text_widget()
        )

        self._code_view.grid(row=0, column=0, sticky=tk.NSEW, in_=self)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._filename = None
        self._last_known_mtime = None

        self._code_view.text.bind("<<Modified>>", self._on_text_modified, True)
        self._code_view.text.bind("<<TextChange>>", self._on_text_change, True)
        self._code_view.text.bind("<Control-Tab>", self._control_tab, True)

        get_workbench().bind("DebuggerResponse", self._listen_debugger_progress, True)
        get_workbench().bind("ToplevelResponse", self._listen_for_toplevel_response, True)

        self.update_appearance()

    def get_text_widget(self):
        return self._code_view.text

    def get_code_view(self):
        # TODO: try to get rid of this
        return self._code_view

    def get_content(self) -> str:
        return self._code_view.get_content()

    def set_filename(self, path):
        self._filename = path

    def get_filename(self, try_hard=False):
        if self._filename is None and try_hard:
            self.save_file()

        return self._filename

    def get_identifier(self):
        if self._filename:
            return self._filename
        else:
            return str(self.winfo_id())

    def get_title(self):
        if self.get_filename() is None:
            result = tr("<untitled>")
        elif is_remote_path(self.get_filename()):
            path = extract_target_path(self.get_filename())
            name = path.split("/")[-1]
            result = "[ " + name + " ]"
        else:
            result = os.path.basename(self.get_filename())

        if self.is_modified():
            result += " *"

        return result

    def check_for_external_changes(self):
        if self._filename is None:
            return

        if is_remote_path(self._filename):
            return

        if self._last_known_mtime is None:
            return

        elif not os.path.exists(self._filename):
            self.master.select(self)

            if messagebox.askyesno(
                    tr("File is gone"),
                    tr("Looks like '%s' was deleted or moved.") % self._filename
                    + "\n\n"
                    + tr("Do you want to also close the editor?"),
                    master=self,
            ):
                self.master.close_editor(self)
            else:
                self.get_text_widget().edit_modified(True)
                self._last_known_mtime = None

        elif os.path.getmtime(self._filename) != self._last_known_mtime:
            skip_confirmation = not self.is_modified() and get_workbench().get_option(
                "edit.auto_refresh_saved_files"
            )
            if not skip_confirmation:
                self.master.select(self)

            if skip_confirmation or messagebox.askyesno(
                    tr("External modification"),
                    tr("Looks like '%s' was modified outside of the editor.") % self._filename
                    + "\n\n"
                    + tr(
                        "Do you want to discard current editor content and reload the file from disk?"
                    ),
                    master=self,
            ):
                prev_location = self.get_text_widget().index("insert")
                self._load_file(self._filename, keep_undo=True)
                try:
                    self.get_text_widget().mark_set("insert", prev_location)
                    self.see_line(int(prev_location.split(".")[0]))
                except Exception:
                    logger.exception("Could not restore previous location")

            self._last_known_mtime = os.path.getmtime(self._filename)

    def get_long_description(self):
        if self._filename is None:
            result = tr("<untitled>")
        else:
            result = self._filename

        try:
            index = self._code_view.text.index("insert")
            if index and "." in index:
                line, col = index.split(".")
                result += "  @  {} : {}".format(line, int(col) + 1)
        except Exception:
            exception("Finding cursor location")

        return result

    def _load_file(self, filename, keep_undo=False):
        try:
            if is_remote_path(filename):
                result = self._load_remote_file(filename)
            else:
                result = self._load_local_file(filename, keep_undo)
                if not result:
                    return False
        except BinaryFileException:
            messagebox.showerror(
                tr("Problem"), tr("%s doesn't look like a text file") % (filename,), master=self
            )
            return False
        except SyntaxError as e:
            assert "encoding" in str(e).lower()
            messagebox.showerror(
                tr("Problem loading file"),
                tr(
                    "This file seems to have problems with encoding.\n\n"
                    "Make sure it is in UTF-8 or contains proper encoding hint."
                ),
                master=self,
            )
            return False

        self.update_appearance()
        return True

    def _load_local_file(self, filename, keep_undo=False):
        with open(filename, "rb") as fp:
            source = fp.read()

        # Make sure Windows filenames have proper format
        filename = normpath_with_actual_case(filename)
        self._filename = filename
        self.update_file_type()
        self._last_known_mtime = os.path.getmtime(self._filename)

        get_workbench().event_generate("Open", editor=self, filename=filename)
        if not self._code_view.set_content_as_bytes(source, keep_undo):
            return False
        self.get_text_widget().edit_modified(False)
        self._code_view.focus_set()
        self.master.remember_recent_file(filename)
        return True

    def _load_remote_file(self, filename):
        self._filename = filename
        self.update_file_type()
        self._code_view.set_content("")
        self._code_view.text.set_read_only(True)

        target_filename = extract_target_path(self._filename)

        self.update_title()
        response = get_runner().send_command_and_wait(
            InlineCommand(
                "read_file", path=target_filename, description=tr("Loading %s") % target_filename
            ),
            dialog_title=tr("Loading"),
        )

        if response.get("error"):
            # TODO: make it softer
            raise RuntimeError(response["error"])

        content = response["content_bytes"]
        self._code_view.text.set_read_only(False)
        if not self._code_view.set_content_as_bytes(content):
            return False
        self.get_text_widget().edit_modified(False)
        self.update_title()
        return True

    def is_modified(self):
        return bool(self._code_view.text.edit_modified())

    def save_file_enabled(self):
        return self.is_modified() or not self.get_filename()

    def save_file(self, ask_filename=False, save_copy=False, node=None) -> Optional[str]:
        if self._filename is not None and not ask_filename:
            save_filename = self._filename
            get_workbench().event_generate("Save", editor=self, filename=save_filename)
        else:
            save_filename = self.ask_new_path(node)

            if not save_filename:
                return None

            if self.containing_notebook.get_editor(save_filename) is not None:
                messagebox.showerror(
                    tr("File is open"),
                    tr(
                        "This file is already open in turcar.\n\n"
                        "If you want to save with this name,\n"
                        "close the existing editor first!"
                    ),
                    master=get_workbench(),
                )
                return None

            get_workbench().event_generate(
                "SaveAs", editor=self, filename=save_filename, save_copy=save_copy
            )

        content_bytes = self._code_view.get_content_as_bytes()

        if is_remote_path(save_filename):
            result = self.write_remote_file(save_filename, content_bytes, save_copy)
        else:
            result = self.write_local_file(save_filename, content_bytes, save_copy)

        if not result:
            return None

        if not save_copy:
            self._filename = save_filename
            self.update_file_type()

        self.update_title()
        return save_filename

    def write_local_file(self, save_filename, content_bytes, save_copy):
        process_shebang = content_bytes.startswith(b"#!/") and get_workbench().get_option(
            "file.make_saved_shebang_scripts_executable"
        )
        if process_shebang:
            content_bytes = content_bytes.replace(b"\r\n", b"\n")

        try:
            f = open(save_filename, mode="wb")
            f.write(content_bytes)
            f.flush()
            # Force writes on disk, see https://learn.adafruit.com/adafruit-circuit-playground-express/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it
            os.fsync(f)
            f.close()
            if process_shebang:
                os.chmod(save_filename, 0o755)
            if not save_copy or save_filename == self._filename:
                self._last_known_mtime = os.path.getmtime(save_filename)
            get_workbench().event_generate(
                "LocalFileOperation", path=save_filename, operation="save"
            )
        except PermissionError:
            messagebox.showerror(
                tr("Permission Error"),
                tr("Looks like this file or folder is not writable."),
                master=self,
            )
            return False

        if not save_copy or save_filename == self._filename:
            self.master.remember_recent_file(save_filename)

        if not save_copy or save_filename == self._filename:
            self._code_view.text.edit_modified(False)

        return True

    def update_file_type(self):
        if self._filename is None:
            self._code_view.set_file_type(None)
        else:
            ext = self._filename.split(".")[-1].lower()
            if ext in PYTHON_EXTENSIONS:
                file_type = "python"
            elif ext in PYTHONLIKE_EXTENSIONS:
                file_type = "pythonlike"
            else:
                file_type = None

            self._code_view.set_file_type(file_type)

        self.update_appearance()

    def write_remote_file(self, save_filename, content_bytes, save_copy):
        if get_runner().ready_for_remote_file_operations(show_message=True):
            target_filename = extract_target_path(save_filename)

            result = get_runner().send_command_and_wait(
                InlineCommand(
                    "write_file",
                    path=target_filename,
                    content_bytes=content_bytes,
                    editor_id=id(self),
                    blocking=True,
                    description=tr("Saving to %s") % target_filename,
                    make_shebang_scripts_executable=get_workbench().get_option(
                        "file.make_saved_shebang_scripts_executable"
                    ),
                ),
                dialog_title=tr("Saving"),
            )

            if "error" in result:
                messagebox.showerror(tr("Could not save"), str(result["error"]))
                return False

            if not save_copy:
                self._code_view.text.edit_modified(False)

            self.update_title()

            # NB! edit_modified is not falsed yet!
            get_workbench().event_generate(
                "RemoteFileOperation", path=target_filename, operation="save"
            )
            get_workbench().event_generate("RemoteFilesChanged")
            return True
        else:
            messagebox.showerror(tr("Could not save"), tr("Back-end is not ready"))
            return False

    def ask_new_path(self, node=None):
        if node is None:
            node = choose_node_for_file_operations(self.winfo_toplevel(), tr("Where to save to?"))
        if not node:
            return None

        if node == "local":
            return self.ask_new_local_path()
        else:
            assert node == "remote"
            return self.ask_new_remote_path()

    def ask_new_remote_path(self):
        target_path = ask_backend_path(self.winfo_toplevel(), "save")
        if target_path:
            target_path = self._check_add_py_extension(target_path)
            return make_remote_path(target_path)
        else:
            return None

    def ask_new_local_path(self):
        if self._filename is None:
            initialdir = get_workbench().get_local_cwd()
            initialfile = None
        else:
            initialdir = os.path.dirname(self._filename)
            initialfile = os.path.basename(self._filename)

        # https://tcl.tk/man/tcl8.6/TkCmd/getOpenFile.htm
        type_var = tk.StringVar(value="")
        new_filename = asksaveasfilename(
            filetypes=_dialog_filetypes,
            defaultextension=None,
            initialdir=initialdir,
            initialfile=initialfile,
            parent=get_workbench(),
            typevariable=type_var,
        )
        logger.info("Save dialog returned %r with typevariable %r", new_filename, type_var.get())

        # Different tkinter versions may return different values
        if new_filename in ["", (), None]:
            return None

        if running_on_windows():
            # may have /-s instead of \-s and wrong case
            new_filename = os.path.join(
                normpath_with_actual_case(os.path.dirname(new_filename)),
                os.path.basename(new_filename),
            )

        if type_var.get() == PYTHON_FILES_STR or type_var.get() == "":
            new_filename = self._check_add_py_extension(
                new_filename, without_asking=type_var.get() == PYTHON_FILES_STR
            )

        if new_filename.endswith(".py"):
            base = os.path.basename(new_filename)
            mod_name = base[:-3].lower()
            if running_on_windows():
                mod_name = mod_name.lower()

            if mod_name in [
                "math",
                "turtle",
                "random",
                "statistics",
                "pygame",
                "matplotlib",
                "numpy",
            ]:
                # More proper name analysis will be performed by ProgramNamingAnalyzer
                if not tk.messagebox.askyesno(
                        tr("Potential problem"),
                        tr(
                            "If you name your script '%s', "
                            "you won't be able to import the library module named '%s'"
                        )
                        % (base, mod_name)
                        + ".\n\n"
                        + tr("Do you still want to use this name for your script?"),
                        master=self,
                ):
                    return self.ask_new_local_path()

        return new_filename

    def show(self):
        self.master.select(self)

    def update_appearance(self):
        self._code_view.set_gutter_visibility(
            get_workbench().get_option("view.show_line_numbers") or get_workbench().in_simple_mode()
        )
        self._code_view.set_line_length_margin(
            get_workbench().get_option("view.recommended_line_length")
        )
        self._code_view.text.update_tabs()
        self._code_view.text.event_generate("<<UpdateAppearance>>")
        self._code_view.grid_main_widgets()

    def _listen_debugger_progress(self, event):
        # Go read-only
        # TODO: check whether this module is active?
        self._code_view.text.set_read_only(True)

    def _listen_for_toplevel_response(self, event: ToplevelResponse) -> None:
        self._code_view.text.set_read_only(False)

    def _control_tab(self, event):
        if event.state & 1:  # shift was pressed
            direction = -1
        else:
            direction = 1
        self.master.select_next_prev_editor(direction)
        return "break"

    def _shift_control_tab(self, event):
        self.master.select_next_prev_editor(-1)
        return "break"

    def select_range(self, text_range):
        self._code_view.select_range(text_range)

    def select_line(self, lineno, col_offset=None):
        self._code_view.select_range(TextRange(lineno, 0, lineno + 1, 0))
        self.see_line(lineno)

        if col_offset is None:
            col_offset = 0

        self.get_text_widget().mark_set("insert", "%d.%d" % (lineno, col_offset))

    def see_line(self, lineno):
        # first see an earlier line in order to push target line downwards
        self._code_view.text.see("%d.0" % max(lineno - 4, 1))
        self._code_view.text.see("%d.0" % lineno)

    def focus_set(self):
        self._code_view.focus_set()

    def is_focused(self):
        return self.focus_displayof() == self._code_view.text

    def _on_text_modified(self, event):
        self.update_title()

    def update_title(self):
        try:
            self.master.update_editor_title(self)
        except Exception:
            logger.exception("Could not update editor title")

    def _on_text_change(self, event):
        # may not be added to the Notebook yet
        if self.containing_notebook.has_content(self):
            self.update_title()

    def destroy(self):
        get_workbench().unbind("DebuggerResponse", self._listen_debugger_progress)
        get_workbench().unbind("ToplevelResponse", self._listen_for_toplevel_response)
        ttk.Frame.destroy(self)
        get_workbench().event_generate(
            "EditorTextDestroyed", editor=self, text_widget=self.get_text_widget()
        )

    def _check_add_py_extension(self, path: str, without_asking: bool = False) -> str:
        assert path
        parts = re.split(r"[/\\]", path)
        name = parts[-1]
        if "." not in name:
            if without_asking or messagebox.askyesno(
                    title=tr("Confirmation"),
                    message=tr("Python files usually have .py extension.")
                            + "\n\n"
                            + tr("Did you mean '%s'?" % (name + ".py")),
                    parent=self.winfo_toplevel(),
            ):
                return path + ".py"
            else:
                return path

        return path


class EditorNotebook(CustomNotebook):
    """
    Manages opened files / modules
    """

    def __init__(self, master):
        super().__init__(master)

        get_workbench().set_default("file.reopen_all_files", False)
        get_workbench().set_default("file.open_files", [])
        get_workbench().set_default("file.current_file", None)
        get_workbench().set_default("file.recent_files", [])
        get_workbench().set_default("view.highlight_current_line", False)
        get_workbench().set_default("view.show_line_numbers", True)
        get_workbench().set_default("view.recommended_line_length", 0)
        get_workbench().set_default("edit.indent_with_tabs", False)
        get_workbench().set_default("edit.auto_refresh_saved_files", True)
        get_workbench().set_default("file.make_saved_shebang_scripts_executable", True)

        self._recent_menu = tk.Menu(
            get_workbench().get_menu("file"), postcommand=self._update_recent_menu
        )
        self._init_commands()
        self.enable_traversal()

        # open files from last session
        """ TODO: they should go only to recent files
        for filename in prefs["open_files"].split(";"):
            if os.path.exists(filename):
                self._open_file(filename)
        """

        # should be in the end, so that it can be detected when
        # constructor hasn't completed yet
        self.preferred_size_in_pw = None
        self._checking_external_changes = False

        get_workbench().bind("WindowFocusIn", self.check_for_external_changes, True)
        get_workbench().bind("ToplevelResponse", self.check_for_external_changes, True)
        self.bind("<<NotebookTabChanged>>", self.on_tab_changed, True)

    def on_tab_changed(self, *args):
        # Required to avoid incorrect sizing of parent panes
        self.update_idletasks()

    def _init_commands(self):
        # TODO: do these commands have to be in EditorNotebook ??
        # Create a module level function install_editor_notebook ??
        # Maybe add them separately, when notebook has been installed ??

        get_workbench().add_command(
            "new_file",
            "file",
            tr("New"),
            self._cmd_new_file,
            caption=tr("New"),
            default_sequence=select_sequence("<Control-n>", "<Command-n>"),
            extra_sequences=["<Control-Greek_nu>"],
            group=10,
            image="new-file",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "open_file",
            "file",
            tr("Open..."),
            self._cmd_open_file,
            caption=tr("Load"),
            default_sequence=select_sequence("<Control-o>", "<Command-o>"),
            extra_sequences=["<Control-Greek_omicron>"],
            group=10,
            image="open-file",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "recents", "file", tr("Recent files"), group=10, submenu=self._recent_menu
        )

        # http://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter
        get_workbench().bind_class("Text", "<Control-o>", self._control_o)
        get_workbench().bind_class("Text", "<Control-Greek_omicron>", self._control_o)
        rebind_control_a(get_workbench())

        get_workbench().add_command(
            "close_file",
            "file",
            tr("Close"),
            self._cmd_close_file,
            default_sequence=select_sequence("<Control-w>", "<Command-w>"),
            extra_sequences=["<Control-Greek_finalsmallsigma>"],
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "close_files",
            "file",
            tr("Close all"),
            self.close_tabs,
            tester=lambda: self.get_current_editor() is not None,
            default_sequence=select_sequence("<Control-W>", "<Command-Alt-w>"),
            group=10,
        )

        get_workbench().add_command(
            "save_file",
            "file",
            tr("Save"),
            self._cmd_save_file,
            caption=tr("Save"),
            default_sequence=select_sequence("<Control-s>", "<Command-s>"),
            extra_sequences=["<Control-Greek_sigma>"],
            tester=self._cmd_save_file_enabled,
            group=10,
            image="save-file",
            include_in_toolbar=True,
        )

        get_workbench().add_command(
            "save_all_files",
            "file",
            tr("Save All files"),
            self._cmd_save_all_files,
            caption=tr("Save All files"),
            default_sequence=select_sequence("<Control-Alt-s>", "<Command-Alt-s>"),
            tester=self._cmd_save_all_files_enabled,
            group=10,
        )

        get_workbench().add_command(
            "save_file_as",
            "file",
            tr("Save as..."),
            self._cmd_save_file_as,
            default_sequence=select_sequence("<Control-Shift-S>", "<Command-Shift-S>"),
            extra_sequences=["<Control-Greek_SIGMA>"],
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "save_copy",
            "file",
            tr("Save copy..."),
            self._cmd_save_copy,
            tester=lambda: self.get_current_editor() is not None,
            group=10,
        )

        get_workbench().add_command(
            "move_rename_file",
            "file",
            tr("Move / rename..."),
            self._cmd_move_rename_file,
            tester=self._cmd_move_rename_file_enabled,
            group=10,
        )

        get_workbench().add_command(
            "goto_source_line",
            "edit",
            tr("Go to line..."),
            self._cmd_goto_source_line,
            default_sequence=select_sequence("<Control-g>", "<Command-g>"),
            # tester=,
            # no global switch, or cross plugin switch?
            # todo use same as find and replace -> plugins/find_replace.py
            group=60,
        )

        get_workbench().add_command(
            "watch_video",
            "course",
            tr("课程更新"),
            self._cmd_course_update,
            caption=tr("Video"),
            group=10,
            image="download1",
            include_in_toolbar=True,
        )

        # get_workbench().add_command(
        #     "watch_video",
        #     "course",
        #     tr("课程视频"),
        #     self._cmd_watch_video,
        #     caption=tr("Video"),
        #     group=10,
        #     image="video",
        #     include_in_toolbar=True,
        # )

        # get_workbench().add_command(
        #     "face_recognition",
        #     "recognition",
        #     tr("百度人脸识别"),
        #     self._cmd_face_recognition,
        #     caption=tr("Recognition"),
        #     group=10,
        #     image="face_recog",
        #     include_in_toolbar=True,
        # )

        get_workbench().add_command(
            "shutdown",
            "help",
            tr("关机"),
            self._cmd_face_shutdown,
            caption=tr("Recognition"),
            default_sequence=select_sequence("<Control-Alt-Delete>", "<Command-Alt-Delete>"),
            group=10,
            image="shutdown",
            include_in_toolbar=True,
        )

        get_workbench().createcommand("::tk::mac::OpenDocument", self._mac_open_document)

    def count_files(self, data):
        count = 0
        for item in data:
            if 'file_url' in item:
                count += 1
            else:
                count += self.count_files(item.get('childer', []))
        return count

    def check_path(self, path):
        if os.path.isdir(path):
            return False
        elif os.path.isfile(path):
            return True
        else:
            return False

    def calculate_md5(self, file_path):
        with open(file_path, 'rb') as file:
            md5 = hashlib.md5()
            while True:
                chunk = file.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
        return md5.hexdigest()

    def update_files_count(self, remote_data, parent_path):
        for remote_item in remote_data:
            remote_name = remote_item['name']
            remote_childer = remote_item.get('childer', [])
            file_name = os.path.join(parent_path, remote_name)
            if not os.path.exists(file_name):
                if 'file_url' in remote_item:
                    self.cy_count += 1
            else:
                check_file = self.check_path(file_name)
                # if check_file:
                #     print('计算的md5', self.calculate_md5(file_name))
            if len(remote_childer):
                self.update_files_count(remote_childer, os.path.join(parent_path, remote_name))

    def check_file(self, path):
        if os.path.isdir(path):
            return False
        else:
            return True

    def remove_files(self, remote_data, parent_path):
        contents = os.listdir(parent_path)
        for item in contents:
            is_file = self.check_file(os.path.join(parent_path, item))
            if is_file:
                flag = False
                for i in remote_data:
                    if i['name'] == item:
                        flag = True
                if not flag:
                    os.remove(os.path.join(parent_path, item))
            else:
                flag = False
                for i in remote_data:
                    if i['name'] == item:
                        flag = True
                        res_path = i.get('childer', [])
                        self.remove_files(res_path, os.path.join(parent_path, item))
                if not flag:
                    self.delete_directory_recursive(os.path.join(parent_path, item))

    def delete_directory_recursive(self,  directory_path):
        if os.path.isdir(directory_path):
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    self.delete_directory_recursive(item_path)
            os.rmdir(directory_path)
            print(f"文件夹 {directory_path} 已删除")
        else:
            print(f"文件夹 {directory_path} 不存在")


    def update_files(self, remote_data, parent_path):
        for remote_item in remote_data:
            remote_name = remote_item['name']
            remote_childer = remote_item.get('childer', [])
            file_name = os.path.join(parent_path, remote_name)
            if not os.path.exists(file_name):
                if not 'file_url' in remote_item:
                    os.makedirs(file_name, exist_ok=True)
                else:
                    self.download_file(remote_item, file_name, str(str(self.cy_current) + '/' + str(self.cy_count)) )
                    self.cy_current += 1
            else:
                check_file = self.check_path(file_name)
                # if check_file:
                #     print('计算的md5', self.calculate_md5(file_name))

            if len(remote_childer):
                self.update_files(remote_childer, os.path.join(parent_path, remote_name))

    def check_internet_connection(self):
        try:
            response = requests.post(self.pull_url)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            return False

    def _cmd_course_update(self):
        self.pull_url = 'http://pyai.yinhangjihua.cn/api/exam/api/sys/fileUpload/first-update'
        if not self.check_internet_connection():
            return messagebox.showerror('无网络', '网络连接失败')

        current_os = platform.system()
        if current_os == "Windows":
            file_path = 'D:\\course'
        else:
            course_name = 'course'
            file_path = os.popen("echo $HOME/"+course_name).read().strip()
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        files = os.listdir(file_path)
        data = requests.post(self.pull_url)
        resp = data.json()['data']['courseDirectoryDTOS']
        self.remote_list = []
        for item in resp:
            chapter_list = item['chapterDirectoryDTOS']
            chapter_list_res = []
            for i in chapter_list:
                content_list = i['contentDTOS']
                content_list_res = []
                for ci in content_list:
                    content_list_res.append({
                        "name": ci['name'],
                        "file_url": ci['path']
                    })
                chapter_list_res.append({
                    "name": i['title'],
                    'childer': content_list_res
                })
            self.remote_list.append({
                "name": item['title'],
                "childer": chapter_list_res
            })
        count = self.count_files(self.remote_list)
        if not files:
            # 第一次，全量更新
            self.current = 1
            message_res = messagebox.askyesno('确定更新', '你确定要更新吗？当前为全量更新，需更新'+str(count) + '个文件')
            if message_res:
                self.create_folder(self.remote_list, file_path, count, self.current)
        else:
            # 差异更新
            self.cy_count = 0
            self.cy_current = 1
            self.remove_files(self.remote_list, file_path)
            self.update_files_count(self.remote_list, file_path)
            if self.cy_count == 0:
                return messagebox.showinfo('无', '暂无更新')
            else:
                message_res = messagebox.askyesno('确定更新',
                                                  '你确定要更新吗？当前为差异更新，需更新' + str(self.cy_count) + '个文件')
                if message_res:
                    self.update_files(self.remote_list, file_path)

    def download_file(self, item, folder_path, str):
        response = requests.get(item['file_url'], stream=True)
        with open(folder_path, 'wb') as f:
            total_length = response.headers.get('content-length')
            if total_length is None:  # 没有内容长度头
                f.write(response.content)
            else:
                self.create_download_progress_view(total_length, f, item, response,
                                                   str)

    def create_folder(self, data, parent_path, count, current):
        for item in data:
            folder_path = os.path.join(parent_path, item['name'])
            if 'file_url' in item:
                # 如果有 file_url 就是文件，直接下载保存到 folder_path
                self.download_file(item, folder_path, str(str(self.current) + '/' + str(count)))
                self.current += 1
            else:
                # 否则就是文件夹，先创建文件夹，再递归调用 create_folder
                os.makedirs(folder_path, exist_ok=True)
                self.create_folder(item['childer'], folder_path, count, self.current)

    def show(self, progress, text):
        if progress == '100.00':
            try:
                self.root.destroy()
            except:
                pass
        else:
            self.progressbarOne['value'] = progress
            self.label.config(text=text)
            self.root.update()

    def null_def(self):
        messagebox.showerror('错误', '禁止关闭')
    def create_download_progress_view(self, total_length, f, item, response, count):
        self.root = tk.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 200
        window_x = int(screen_width / 2 - window_width / 2)
        window_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
        self.root.title('资料更新')
        self.root.protocol("WM_DELETE_WINDOW", self.null_def)
        self.div = tk.Frame(self.root)
        self.div.place(relx=0.5,rely=0.5,anchor='center')

        self.progressbarOne = ttk.Progressbar(self.div)


        self.progressbarOne.pack()
        # 进度值最大值
        self.progressbarOne['maximum'] = 100
        # 进度值初始值
        self.progressbarOne['value'] = 0
        self.progressbarOne['length'] = 480

        self.label = tk.Label(self.div)
        self.label.pack(pady=20)

        self.label1 = tk.Label(self.div, text=count)
        self.label1.pack(pady=10)

        downloaded = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            downloaded += len(data)
            f.write(data)
            status = response.status_code
            if status != 200:
                print(f"下载失败: {status}")
                break
            if total_length != 0:
                pro = "{:.2f}".format(downloaded / total_length * 100)
            else:
                pro = "0.00"
            self.show(pro, '当前下载文件为--' + item['name'] + '--,' + "进度为:--" + str(pro) + '%--')
    def load_startup_files(self):
        """If no filename was sent from command line
        then load previous files (if setting allows)"""

        cmd_line_filenames = [
            os.path.abspath(name) for name in sys.argv[1:] if os.path.exists(name)
        ]

        if len(cmd_line_filenames) > 0:
            filenames = cmd_line_filenames
        elif get_workbench().get_option("file.reopen_all_files"):
            filenames = get_workbench().get_option("file.open_files")
        elif get_workbench().get_option("file.current_file"):
            filenames = [get_workbench().get_option("file.current_file")]
        else:
            filenames = []

        if len(filenames) > 0:
            for filename in filenames:
                if os.path.exists(filename):
                    self.show_file(filename)

            cur_file = get_workbench().get_option("file.current_file")
            # choose correct active file
            if len(cmd_line_filenames) > 0:
                self.show_file(cmd_line_filenames[0])
            elif cur_file and os.path.exists(cur_file):
                self.show_file(cur_file)
            else:
                self._cmd_new_file()
        else:
            self._cmd_new_file()

    def save_all_named_editors(self):
        all_saved = True
        for editor in self.winfo_children():
            if editor.get_filename() and editor.is_modified():
                success = editor.save_file()
                all_saved = all_saved and success

        return all_saved

    def remember_recent_file(self, filename):
        recents = get_workbench().get_option("file.recent_files")
        if filename in recents:
            recents.remove(filename)
        recents.insert(0, filename)
        relevant_recents = [name for name in recents if os.path.exists(name)][:15]
        get_workbench().set_option("file.recent_files", relevant_recents)
        get_workbench().set_option('general.ui_mode', 'regular')
        self._update_recent_menu()

    def _update_recent_menu(self):
        recents = get_workbench().get_option("file.recent_files")
        relevant_recents = [
            path for path in recents if os.path.exists(path) and not self.file_is_opened(path)
        ]
        self._recent_menu.delete(0, "end")
        for path in relevant_recents:
            def load(path=path):
                self.show_file(path)

            self._recent_menu.insert_command("end", label=path, command=load)

    def remember_open_files(self):
        if (
                self.get_current_editor() is not None
                and self.get_current_editor().get_filename() is not None
        ):
            current_file = self.get_current_editor().get_filename()
        else:
            current_file = None

        get_workbench().set_option("file.current_file", current_file)

        open_files = [
            editor.get_filename() for editor in self.winfo_children() if editor.get_filename()
        ]
        get_workbench().set_option("file.open_files", open_files)

    def _cmd_new_file(self):
        self.open_new_file()

    def open_new_file(self, path=None, remote=False):
        new_editor = Editor(self)
        get_workbench().event_generate("NewFile", editor=new_editor)
        if path:
            if remote:
                new_editor.set_filename(make_remote_path(path))
            else:
                new_editor.set_filename(path)
        self.add(new_editor, text=new_editor.get_title())
        self.select(new_editor)
        new_editor.focus_set()

    def _cmd_open_file(self):
        node = choose_node_for_file_operations(self.winfo_toplevel(), "Where to open from?")
        if not node:
            return

        if node == "local":
            initialdir = get_workbench().get_local_cwd()
            if (
                    self.get_current_editor() is not None
                    and self.get_current_editor().get_filename() is not None
            ):
                initialdir = os.path.dirname(self.get_current_editor().get_filename())
            path = askopenfilename(
                filetypes=_dialog_filetypes, initialdir=initialdir, parent=get_workbench()
            )
        else:
            assert node == "remote"
            target_path = ask_backend_path(self.winfo_toplevel(), "open")
            if not target_path:
                return

            path = make_remote_path(target_path)

        if path:
            # self.close_single_untitled_unmodified_editor()
            self.show_file(path, propose_dialog=False)

    def _control_o(self, event):
        # http://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter
        self._cmd_open_file()
        return "break"

    def _close_files(self, except_index=None):
        for tab_index in reversed(range(len(self.winfo_children()))):
            if except_index is not None and tab_index == except_index:
                continue
            else:
                editor = self.get_child_by_index(tab_index)
                self.close_editor(editor, force=False)

    def _cmd_close_file(self):
        self.close_tab(self.index(self.select()))

    def close_tab(self, index_or_tab: Union[int, CustomNotebookTab]):
        if isinstance(index_or_tab, int):
            page = self.pages[index_or_tab]
        else:
            page = self.get_page_by_tab(index_or_tab)

        # assert isinstance(page.content, Editor)
        self.close_editor(page.content)

    def close_editor(self, editor, force=False):
        if not force and not self.check_allow_closing(editor):
            return
        self._plain_forget(editor)
        editor.destroy()

    def _cmd_save_file(self):
        if self.get_current_editor():
            self.get_current_editor().save_file()
            self.update_editor_title(self.get_current_editor())

    def _cmd_save_file_enabled(self):
        return self.get_current_editor() and self.get_current_editor().save_file_enabled()

    def _cmd_save_all_files(self):
        for editor in self.get_all_editors():
            if editor.save_file_enabled() == True:
                editor.save_file()
                self.update_editor_title(editor)

    def _cmd_save_all_files_enabled(self):
        for editor in self.get_all_editors():
            if editor.save_file_enabled() == True:
                return True
        return False

    def _cmd_save_file_as(self, node=None):
        if not self.get_current_editor():
            return

        self.get_current_editor().save_file(ask_filename=True, node=node)
        self.update_editor_title(self.get_current_editor())
        get_workbench().update_title()

    def _cmd_save_copy(self):
        if not self.get_current_editor():
            return

        self.get_current_editor().save_file(ask_filename=True, save_copy=True)
        self.update_editor_title(self.get_current_editor())

    def _cmd_save_file_as_enabled(self):
        return self.get_current_editor() is not None

    def _cmd_move_rename_file(self):
        editor = self.get_current_editor()
        old_filename = editor.get_filename()
        assert old_filename is not None

        if is_remote_path(old_filename):
            node = "remote"
        else:
            node = "local"

        self._cmd_save_file_as(node=node)

        if editor.get_filename() != old_filename:
            if is_remote_path(old_filename):
                remote_path = extract_target_path(old_filename)
                get_runner().send_command_and_wait(
                    InlineCommand(
                        "delete", paths=[remote_path], description=tr("Deleting" + remote_path)
                    ),
                    dialog_title=tr("Deleting"),
                )
                get_workbench().event_generate(
                    "RemoteFileOperation", path=remote_path, operation="delete"
                )
            else:
                os.remove(old_filename)
                get_workbench().event_generate(
                    "LocalFileOperation", path=old_filename, operation="delete"
                )

    def _cmd_move_rename_file_enabled(self):
        return self.get_current_editor() and self.get_current_editor().get_filename() is not None

    def close_single_untitled_unmodified_editor(self):
        editors = self.winfo_children()
        if len(editors) == 1 and not editors[0].is_modified() and not editors[0].get_filename():
            self._cmd_close_file()

    def _cmd_goto_source_line(self):
        editor = self.get_current_editor()
        if editor:
            line_no = simpledialog.askinteger(tr("Go to line"), tr("Line number"))
            if line_no:
                editor.select_line(line_no)

    def _mac_open_document(self, *args):
        for arg in args:
            if isinstance(arg, str) and os.path.exists(arg):
                self.show_file(arg)
        get_workbench().become_active_window()

    def get_current_editor(self) -> Optional[Editor]:
        return self.get_current_child()

    def get_current_editor_content(self):
        editor = self.get_current_editor()
        if editor is None:
            return None
        else:
            return editor.get_content()

    def get_all_editors(self):
        # When workspace is closing, self.winfo_children()
        # may return an unexplainable tkinter.Frame
        return [child for child in self.winfo_children() if isinstance(child, Editor)]

    def select_next_prev_editor(self, direction):
        cur_index = self.index(self.select())
        next_index = (cur_index + direction) % len(self.tabs())
        self.select(self.get_child_by_index(next_index))

    def file_is_opened(self, path):
        for editor in self.get_all_editors():
            if editor.get_filename() and is_same_path(path, editor.get_filename()):
                return True

        return False

    def show_file(self, filename, text_range=None, set_focus=True, propose_dialog=True):
        # self.close_single_untitled_unmodified_editor()
        try:
            editor = self.get_editor(filename, True)
        except PermissionError:
            logger.exception("Loading " + filename)
            msg = tr("Got permission error when trying to load\n%s") % (filename,)
            if running_on_mac_os() and propose_dialog:
                msg += "\n\n" + tr("Try opening it with File => Open.")

            messagebox.showerror(tr("Permission error"), msg, master=self)
            return None

        if editor is None:
            return

        self.select(editor)
        if set_focus:
            editor.focus_set()

        if text_range is not None:
            editor.select_range(text_range)

        return editor

    def show_remote_file(self, target_filename):
        if not get_runner().ready_for_remote_file_operations(show_message=True):
            return None
        else:
            return self.show_file(make_remote_path(target_filename))

    # 获取视频
    def _cmd_watch_video(self):
        # print("sss")
        # ui_utils.show_dialog(VideoDialog(get_workbench()))
        get_workbench().show_view("VideoPlay")
        get_workbench().event_generate("VideoPlay")
    def _cmd_face_shutdown(self):
        result = messagebox.askokcancel("确认关机", "您确定要关机吗？")
        if result:
            print('关机了')
            os.popen("poweroff").read()
        else:
            print('取消关机了')
    # 人脸识别
    def _cmd_face_recognition(self):
        pass
        # # 获取当前操作系统
        # current_os = platform.system()
        #
        # if current_os == "Windows":
        #     save_path = "D:/copy.png"
        #     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 打开笔记本内置摄像头
        # if current_os == "Darwin":  # 默认为Ubuntu或其他Linux发行版
        #     save_path = "turcar/copy.png"
        #     cap = cv2.VideoCapture(0)
        # else:
        #     # todo Ubuntu摄像头获取失败
        # pass
        #
        # while cap.isOpened():  # 笔记本内置摄像头被打开后
        #     ret, frame = cap.read()  # 从摄像头中实时读取视频
        #     cv2.imshow("Recognition", frame)  # 在窗口中显示视频
        #     k = cv2.waitKey(1)  # 图像的刷新时间为1毫秒
        #     if k == ord(' '):  # 按下空格键
        #         cv2.imshow('img', frame)  # 显示按下空格键时摄像头视频中的图像
        #         cv2.imwrite(save_path, frame)  # 保存按下空格键时摄像头视频中的图像
        #         cap.release()  # 关闭笔记本内置摄像头
        #         cv2.destroyWindow("Recognition")  # 销毁名为Video的窗口
        #         break
        # cv2.destroyAllWindows()  # 销毁显示图像的窗口
        # url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + get_access_token()
        #
        # # image 可以通过 get_file_content_as_base64("C:\fakepath\多人二维码.jpg",False) 方法获取
        # # path = r"D:/copy.png"
        # image = get_file_content_as_base64(save_path, False)
        # payload = json.dumps({
        #     "image": image,
        #     "image_type": "BASE64",
        #     "face_field": "age,expression,face_shape,gender,glasses,emotion,mask",
        #     "max_face_num": 100
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # # 解析response为JSON格式
        # response_data = json.loads(response.text)
        # error_code = response_data["error_code"]
        # timestamp = response_data["timestamp"]
        # dt = datetime.datetime.fromtimestamp(timestamp)
        # # 将datetime对象转换为指定格式的字符串
        # formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
        # root = tk.Tk()
        # root.withdraw()  # 隐藏主窗口
        # if error_code == 0:
        #     # 获取face_num等字段
        #     face_num = response_data['result']['face_num']
        #     face_list_text = f"人脸信息列表：\n"
        #     if face_num > 0:
        #         face_list = response_data['result']['face_list']
        #         print(face_list)
        #         # 遍历列表中的字典
        #         for item in face_list:
        #             face_probability = item['face_probability']
        #             age = item["age"]
        #             expression = self.determine_expression(item['expression'])
        #             face_shape = self.determine_face_shape(item['face_shape'])
        #             gender = self.determine_gender(item['gender']['type'])
        #             glasses = self.determine_glasses(item['glasses'])
        #             emotion = self.determine_emotion(item['emotion'])
        #             mask = self.determine_mask(item['mask'])
        #             item_text = f"[\n" \
        #                         f" 人脸置信度（0—1）：{face_probability}\n" \
        #                         f" 年龄：{age}\n" \
        #                         f" 表情：{expression}\n" \
        #                         f" 脸型：{face_shape}\n" \
        #                         f" 性别：{gender}\n" \
        #                         f" 是否戴眼镜：{glasses}\n" \
        #                         f" 情绪：{emotion}\n" \
        #                         f" 口罩：{mask}\n" \
        #                         f"]\n"
        #             face_list_text = face_list_text + item_text
        #
        #     messagebox.askokcancel("识别结果", f"识别成功,时间：{formatted_datetime}"
        #                                        f"\n检测到的图片中的人脸数量：{face_num}"
        #                                        f"\n{face_list_text}")
        #
        # else:
        #     messagebox.askokcancel("识别结果", "请求失败")
        # return response

    def determine_gender(self, gender):
        return '男' if gender == 'male' else '女'

    def determine_expression(self, expression):
        if expression["type"] == "none":
            return "不笑", '置信度:' + str(expression["probability"])
        elif expression["type"] == "smile":
            return "微笑",'置信度:' + str(expression["probability"])
        elif expression["type"] == "laugh":
            return "大笑", '置信度:' + str(expression["probability"])
        else:
            return "无法确定", 0
    def determine_face_shape(self, face_shape):
        if face_shape["type"] == "square":
            return "正方形", '置信度:' + str(face_shape["probability"])
        elif face_shape["type"] == "triangle":
            return "三角形",'置信度:' + str(face_shape["probability"])
        elif face_shape["type"] == "oval":
            return "椭圆", '置信度:' + str(face_shape["probability"])
        elif face_shape["type"] == "heart":
            return "心形", '置信度:' + str(face_shape["probability"])
        elif face_shape["type"] == "round":
            return "圆形", '置信度:' + str(face_shape["probability"])
        else:
            return "无法确定", 0
    def determine_glasses(self, glasses):
        if glasses["type"] == "none":
            return "无眼镜", '置信度:' + str(glasses["probability"])
        elif glasses["type"] == "common":
            return "普通眼镜",'置信度:' + str(glasses["probability"])
        elif glasses["type"] == "sun":
            return "墨镜", '置信度:' + str(glasses["probability"])
        else:
            return "无法确定", 0
    def determine_mask(self, mask):
        if mask["type"] == 0:
            return "没戴口罩", '置信度:' + str(mask["probability"])
        elif mask["type"] == 1:
            return "戴口罩",'置信度:' + str(mask["probability"])
        else:
            return "无法确定", 0
    def determine_emotion(self, emotion):
        if emotion["type"] == "angry":
            return "愤怒", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "disgust":
            return "厌恶",'置信度:' + str(emotion["probability"])
        elif emotion["type"] == "fear":
            return "恐惧", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "happy":
            return "高兴", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "sad":
            return "伤心", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "surprise":
            return "惊讶", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "neutral":
            return "无表情", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "pouty":
            return "噘嘴", '置信度:' + str(emotion["probability"])
        elif emotion["type"] == "grimace":
            return "鬼脸", '置信度:' + str(emotion["probability"])
        else:
            return "无法确定", 0

    def show_file_at_line(self, filename, lineno, col_offset=None):
        editor = self.show_file(filename)
        editor.select_line(lineno, col_offset)

    def update_appearance(self):
        for editor in self.winfo_children():
            editor.update_appearance()

    def update_editor_title(self, editor, title=None):
        if title is None:
            title = editor.get_title()
        try:
            self.tab(editor, text=title)
        except TclError:
            pass

        try:
            self.indicate_modification()
        except Exception:
            logger.exception("Could not update modification indication")

    def indicate_modification(self):
        if not running_on_mac_os():
            return

        atts = self.winfo_toplevel().wm_attributes()
        if "-modified" in atts:
            i = atts.index("-modified")
            mod = atts[i: i + 2]
            rest = atts[:i] + atts[i + 2:]
        else:
            mod = ()
            rest = atts

        for editor in self.get_all_editors():
            if editor.is_modified():
                if mod != ("-modified", 1):
                    self.winfo_toplevel().wm_attributes(*(rest + ("-modified", 1)))
                break
        else:
            if mod == ("-modified", 1):
                self.winfo_toplevel().wm_attributes(*(rest + ("-modified", 0)))

    def _open_file(self, filename):
        editor = Editor(self)
        if editor._load_file(filename):
            self.add(editor, text=editor.get_title())
            return editor
        else:
            editor.destroy()
            return None

    def get_editor(self, filename_or_id, open_when_necessary=False):
        if os.path.isfile(filename_or_id):
            filename_or_id = normpath_with_actual_case(os.path.abspath(filename_or_id))

        for child in self.winfo_children():
            assert isinstance(child, Editor)
            child_identifier = child.get_identifier()
            if child_identifier == filename_or_id:
                return child

        if open_when_necessary:
            return self._open_file(filename_or_id)
        else:
            return None

    def check_allow_closing(self, editor=None):
        if not editor:
            modified_editors = [e for e in self.winfo_children() if e.is_modified()]
        else:
            if not editor.is_modified():
                return True
            else:
                modified_editors = [editor]
        if len(modified_editors) == 0:
            return True

        message = tr("Do you want to save files before closing?")
        if editor:
            message = tr("Do you want to save file before closing?")

        confirm = messagebox.askyesnocancel(
            title=tr("Save On Close"), message=message, default=messagebox.YES, master=self
        )

        if confirm:
            for editor_ in modified_editors:
                assert isinstance(editor_, Editor)
                if editor_.get_filename(True):
                    if not editor_.save_file():
                        return False
                else:
                    return False
            return True

        elif confirm is None:
            return False
        else:
            return True

    def check_for_external_changes(self, event=None):
        if self._checking_external_changes:
            # otherwise the method will be re-entered when focus
            # changes because of a confirmation message box
            return

        self._checking_external_changes = True
        try:
            for editor in self.get_all_editors():
                editor.check_for_external_changes()
        finally:
            self._checking_external_changes = False


# 百度智能云人脸识别
API_KEY = "bo0Tfin2s2Lc3DUVQW3DzOPb"
SECRET_KEY = "DbF0dvfAOW9aLG5Izi1EI3RsVprBwuXp"


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_current_breakpoints():
    result = {}

    for editor in get_workbench().get_editor_notebook().get_all_editors():
        filename = editor.get_filename()
        if filename:
            linenos = editor.get_code_view().get_breakpoint_line_numbers()
            if linenos:
                result[filename] = linenos

    return result


def get_saved_current_script_filename(force=True):
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if not editor:
        return None

    filename = editor.get_filename(force)
    if not filename:
        return None

    if editor.is_modified():
        filename = editor.save_file()

    return filename


def get_target_dirname_from_editor_filename(s):
    if is_local_path(s):
        return os.path.dirname(s)
    else:
        return universal_dirname(extract_target_path(s))


def extract_target_path(s):
    assert is_remote_path(s)
    return s[s.find(REMOTE_PATH_MARKER) + len(REMOTE_PATH_MARKER):]


def make_remote_path(target_path):
    return get_runner().get_node_label() + REMOTE_PATH_MARKER + target_path
