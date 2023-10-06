import customtkinter as ctk
import tkinter as tk
import werkzeug.security as ws


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unit 5");
        self.geometry("400x300");
        self.resizable(False, False)

        self._screen = None
        self.change_screen(StartPage(self))

    def change_screen(self, new_screen):
        if self._screen is not None:
            self._screen.destroy()
        self._screen = new_screen


class Screen(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master=master)
        self.title_label = ctk.CTkLabel(self, text=title)
        self.title_label.grid(column=0, row=0)

        self.content = ctk.CTkFrame(master=master)
        self.content.grid(column=0, row=1, padx=(5, 5), pady=(5, 5), sticky="NESW")


class StartPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Welcome")

        self.username = tk.StringVar(self.content)
        self.password = tk.StringVar(self.content)

        ctk.CTkLabel(self.content, text="Username").grid(row=0, column=0)
        username = ctk.CTkEntry(self.content, textvariable=self.username).grid(row=0, column=1)
        ctk.CTkLabel(self.content, text="Password").grid(row=1, column=0)
        password = ctk.CTkEntry(self.content, textvariable=self.password, show='●').grid(row=1, column=1)
        ctk.CTkButton(self.content, text="Login", command=lambda: self.login(self.username.get(), self.password.get())).grid(row=2, column=0)

    def login(self, username, password):
        print(username)
        password_hash = ws.generate_password_hash(password=password, salt_length=24)
        print(password_hash)


class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self.content, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(self.content, text="Open start page",
                      command=lambda: master.change_screen(StartPage(master))).grid(row=1, column=0)
