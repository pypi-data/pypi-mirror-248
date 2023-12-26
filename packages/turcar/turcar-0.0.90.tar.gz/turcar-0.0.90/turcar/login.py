import os
import tkinter as tk
import sys
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


import mysql.connector.pooling

user_table = "sys_user"
# 创建MySQL连接池
config = {
    "user": "root",
    "password": "aY)I&iBop[F3t",
    "host": "180.76.235.69",
    "port": "3306",
    "database": "pyai",
    "auth_plugin": "mysql_native_password",
}

db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **config)


# 开启连接
def open_connection():
    # 创建数据库连接
    db_connection = db_pool.get_connection()
    return db_connection


# 关闭连接
def close_connection(cursor, db_connection):
    # 关闭游标和连接
    cursor.close()
    db_connection.close()


class UserLogin:
    def __init__(self):
        self.account = None
        self.password = None
        self.login_image = None
        self.root = tk.Tk()
        self.login_result = False
        self.canvas = None
        self.bg_img = None
        self.account_var = None
        self.account_entry = None

        # 添加"密码："标签和输入框
        self.password_var = None
        self.password_entry = None
        self.root.bind("<KeyPress-Return>", lambda event: self.login())  # 绑定回车键

        self.root.protocol("WM_DELETE_WINDOW", self.null_def)

    # def login(self):
    #     userService = UserService()
    #     account = self.account_var.get()
    #     password = self.password_var.get()
    #
    #     # 校验账号和密码
    #     if not account:
    #         messagebox.showerror("登录结果", "账号不能为空")
    #         return
    #         # 校验手机号码
    #     pattern = r'^1[3457896]\d{9}$'
    #     if not re.match(pattern, account):
    #         messagebox.showerror(title='This is the title', message="电话号码错误", detail='请输入有效的电话号码',
    #                              icon=messagebox.ERROR)
    #         # for child in self.fr.winfo_children():
    #         #     child.configure(state="normal")
    #         self.account_entry.config(state="normal")  # 设置账号输入框为可编辑状态
    #         self.password_entry.config(state="normal")  # 设置密码输入框为可编辑状态
    #
    #         return
    #
    #     if not password:
    #         messagebox.showerror("登录结果", "密码不能为空")
    #         return
    #
    #     if len(password) < 6:
    #         messagebox.showerror("登录结果", "密码不能少于六位")
    #         return
    #     # 执行登录逻辑
    #     if userService.login(account, password):
    #         self.login_result = True
    #         self.on_closing()
    #     else:
    #         # self.config(state="normal")
    #         messagebox.showerror(title="Show Error", message="账号密码错误")

    def login(self):
        db_connection = open_connection()
        cursor = db_connection.cursor(dictionary=True)
        account = self.account_var.get()
        password = self.password_var.get()

        # 校验账号和密码
        if not account:
            messagebox.showerror("登录结果", "账号为身份证后6位，不能为空,")
            return
            # 校验手机号码

        if not password:
            messagebox.showerror("登录结果", "密码为手机号后4位，不能为空")
            return

        if len(password) != 4:
            messagebox.showerror("登录结果", "密码为手机号后4位")
            return

        # query_sql = f"SELECT COUNT(*) FROM '{user_table}' WHERE account = '{account}' AND password = '{password}'"
        query_sql = f"SELECT COUNT(*) FROM {user_table} WHERE SUBSTRING(id_card_num, LENGTH(id_card_num)-5) = {account} AND SUBSTRING(user_name, LENGTH(user_name)-3) ={password}"
        cursor.execute(query_sql)
        fetchone = cursor.fetchone()
        print(fetchone)
        existUser = fetchone['COUNT(*)']
        if existUser > 0:
            query_sql = f"SELECT COUNT(*) FROM {user_table} WHERE SUBSTRING(id_card_num, LENGTH(id_card_num)-5) = {account} AND SUBSTRING(user_name, LENGTH(user_name)-3) = {password} AND state = 1"
            cursor.execute(query_sql)
            fetchone = cursor.fetchone()
            existUser = fetchone['COUNT(*)']
            if existUser > 0:
                self.login_result = True
                self.on_closing()
            else:
                messagebox.showerror(title="Show Error",
                                     message="账号未审核,请先联系管理员审核")

        else:
            query_sql = f"SELECT COUNT(*) FROM {user_table} WHERE SUBSTRING(id_card_num, LENGTH(id_card_num)-5) = {account}"
            cursor.execute(query_sql)
            fetchone = cursor.fetchone()
            print(fetchone)
            existUser = fetchone['COUNT(*)']
            if existUser > 0:
                messagebox.showerror(title="Show Error", message="密码错误,密码为手机号后4位")
            else:
                messagebox.showerror(title="Show Error",
                                     message="账号错误,账号为身份证后6位,若无账户请先前往公众号注册")

        close_connection(cursor, db_connection)

    def get_current_os(self):
        platform = sys.platform
        if platform.startswith('win'):
            return "Windows"
        elif platform.startswith('linux'):
            return "Linux"
        elif platform == 'darwin':
            return "Mac"
        else:
            return "Unknown"

    def create_login_view(self):
        root = self.root
        root.title("引航计划")
        # root.resizable(width=False, height=False)
        # root.attributes('-fullscreen', True)  # 隐藏标题栏
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)
        system_type = self.get_current_os()
        if system_type == 'Windows':
            root.wm_attributes("-toolwindow", True)
        elif system_type == 'Linux':
            root.protocol("WM_ICONIFY", self.null_def)
            root.bind("<Unmap>", self.null_def)
        login_bg = os.path.join(os.path.dirname(__file__), "res", "login-poster.png")
        self.bg_img = Image.open(login_bg)
        self.bg_img = self.bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        # Create a background image item on the canvas and set its anchor to 'nw'
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw", tags="bg")
        self.canvas.config(highlightthickness=0)

        # 获取 Canvas 的宽度和高度
        canvas_width = root.winfo_screenwidth()
        canvas_height = root.winfo_screenheight()

        img_dir = os.path.join(os.path.dirname(__file__), "res", "login_logo.png")
        original_image = Image.open(img_dir)
        resized_image = original_image.resize((320, 130), Image.LANCZOS)  # Resize to 100x100
        self.login_image = ImageTk.PhotoImage(resized_image)
        # 获取图像的宽度和高度
        image_width = self.login_image.width()
        image_height = self.login_image.height()

        # 计算图像在 Canvas 上居中的位置
        x = (canvas_width - image_width) / 2
        y = (canvas_height - image_height) / 2
        self.canvas.create_image(x, y - 150, image=self.login_image, anchor="nw")
        # 添加"账号："标签和输入框
        self.canvas.create_text(x + 40, y + 15, text="账号：".encode("utf-8").decode("utf-8"), anchor="nw")
        self.account_var = tk.StringVar()
        self.account_entry = ttk.Entry(self.canvas, textvariable=self.account_var)
        self.canvas.create_window(x + 190, y + 28, window=self.account_entry)
        # self.account_entry.place(relx=0.46, rely=0.452, relwidth=0.11, relheight=0.025)

        # 添加"密码："标签和输入框
        self.canvas.create_text(x + 40, y + 65, text="密码：".encode("utf-8").decode("utf-8"), anchor="nw")
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.canvas, show="*", textvariable=self.password_var)
        self.canvas.create_window(x + 190, y + 75, window=self.password_entry)

        button = ttk.Button(self.canvas, text="登录".encode("utf-8").decode("utf-8"), command=self.login)
        self.account_entry.configure(state="normal")
        self.password_entry.configure(state="normal")
        self.canvas.create_window(x + 160, y + 140, window=button)

        root.mainloop()

    def on_closing(self):
        self.root.destroy()  # 销毁窗口

    def null_def(self):
        pass
