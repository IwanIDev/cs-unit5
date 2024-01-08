from tkinter import messagebox

import customtkinter as ctk
import tkinter as tk
import login_manager
from database import database


class Screen(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master=master, fg_color=master.cget("bg"))
        self.title_label = ctk.CTkLabel(self.master, text=title)
        self.title_label.grid(column=0, row=0)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unit 5")
        self.geometry("400x300")
        self.resizable(False, False)

        self._screen = None
        self.change_screen(StartPage(self))

        self.grid_propagate(False)

    def change_screen(self, new_screen: Screen):
        if self._screen is not None:
            self._screen.destroy()
        self._screen = new_screen.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))


class StartPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Welcome")

        self.username = tk.StringVar(self)
        self.password = tk.StringVar(self)

        ctk.CTkLabel(self, text="Username").grid(row=0, column=0)
        ctk.CTkEntry(self, textvariable=self.username).grid(row=0, column=1)
        ctk.CTkLabel(self, text="Password").grid(row=1, column=0)
        ctk.CTkEntry(self, textvariable=self.password, show="●").grid(row=1, column=1)

        ctk.CTkButton(
            self,
            text="Register",
            command=self.register_user,
        ).grid(row=2, column=1, pady=(5, 5))

        ctk.CTkButton(
            self,
            text="Login",
            command=self.login_user
        ).grid(row=3, column=1, pady=(5, 5))

    def login_user(self):
        result, success = login_manager.login_user(username=self.username.get(), password=self.password.get(), database=database)
        if not success:
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Login successful", message=f"Login was successful.")

    def register_user(self):
        result = login_manager.register_user(username=self.username.get(),
                                             password=self.password.get(),
                                             database=database)
        if isinstance(result, str):
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Data entered", message="Data entered into database!")


class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(
            self,
            text="Open start page",
            command=lambda: master.change_screen(StartPage(master)),
        ).grid(row=1, column=0)
