import customtkinter as ctk
import tkinter as tk
import login_manager


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unit 5");
        self.geometry("400x300");
        self.resizable(False, False)

        self._screen = None
        self.change_screen(StartPage(self))

        self.grid_propagate(False)

    def change_screen(self, new_screen):
        if self._screen is not None:
            self._screen.destroy()
        self._screen = new_screen.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))


class Screen(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master=master, fg_color=master.cget("bg"))
        self.title_label = ctk.CTkLabel(self.master, text=title)
        self.title_label.grid(column=0, row=0)


class StartPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Welcome")

        self.username = tk.StringVar(self)
        self.password = tk.StringVar(self)

        ctk.CTkLabel(self, text="Username").grid(row=0, column=0)
        username = ctk.CTkEntry(self, textvariable=self.username).grid(row=0, column=1, pady=(5, 5))
        ctk.CTkLabel(self, text="Password").grid(row=1, column=0)
        password = ctk.CTkEntry(self, textvariable=self.password, show='●').grid(row=1, column=1)

        ctk.CTkButton(self, text="Login",
                      command=lambda: login_manager.register_user(self.username.get(), self.password.get())).grid(
            row=2, column=1, pady=(5, 5)
        )


class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(self, text="Open start page",
                      command=lambda: master.change_screen(StartPage(master))).grid(row=1, column=0)
