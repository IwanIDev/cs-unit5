import customtkinter as ctk, tkinter as tk, werkzeug.security as ws

test = ws.generate_password_hash("hi");
valid = ws.check_password_hash(test, "test");
print(test);
print(valid)


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
        self.username = ""
        self.password = ""

        super().__init__(master=master, title="Welcome")
        ctk.CTkLabel(self.content, text="Username").grid(row=0, column=0)
        username = ctk.CTkEntry(self.content, textvariable=self.username).grid(row=0, column=1)
        ctk.CTkLabel(self.content, text="Password").grid(row=1, column=0)
        password = ctk.CTkEntry(self.content, textvariable=self.password, show='*').grid(row=1, column=1)


class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self.content, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(self.content, text="Open start page",
                      command=lambda: master.change_screen(StartPage(master))).grid(row=1, column=0)
