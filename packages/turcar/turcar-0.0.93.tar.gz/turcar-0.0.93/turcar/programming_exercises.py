import logging
import threading
import tkinter as tk
from tkinter import ttk
from turcar import get_workbench
from turcar.languages import tr
from cefpython3 import cefpython as cef
import sys

logger = logging.getLogger(__name__)


# 浏览器内容窗口
class CefBrowser(ttk.Frame):
    def __init__(self, parent=None):
        self.browser = None
        super().__init__(parent)


class InnerBrowser(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master, style="ViewBody.TFrame")

        self.text_command = tk.Text(self, width=160, height=1)
        default_text = "http://180.76.235.69"
        self.text_command.insert("1.0", default_text)

        rect = [0, 50, 1200, 1000]
        self.thread = threading.Thread(target=self.embed_browser_thread, args=(self, rect, default_text))
        self.thread.start()
        self.browser_widget = CefBrowser()

    def initialize_cef(self):
        rect = [0, 50, 1200, 1000]
        default_text = "http://180.76.235.69"
        self.thread = threading.Thread(target=self.embed_browser_thread, args=(self, rect, default_text))
        self.thread.start()
        self.browser_widget = CefBrowser()

    def close_cef(self):
        cef.Shutdown()

    def open_programming_exercises(self):
        rect = [0, 0, 800, 600]
        default_text = self.text_command.get("1.0", "end-1c")
        self.embed_browser_thread(self, rect, default_text)

    def embed_browser_thread(self, frame, _rect, url):
        sys.excepthook = cef.ExceptHook
        window_info = cef.WindowInfo(frame.winfo_id())
        window_info.SetAsChild(frame.winfo_id(), _rect)
        cef.Initialize()
        self.browser_widget.browser = cef.CreateBrowserSync(window_info, url=url)
        cef.MessageLoop()
        cef.Shutdown()


def init() -> None:
    get_workbench().add_view(InnerBrowser, tr("programming_exercises"), "se")
