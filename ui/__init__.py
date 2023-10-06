import customtkinter as ctk
import tkinter as tk
import werkzeug.security as ws
import httpx


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
                      command=lambda: self.login(self.username.get(), self.password.get())).grid(
            row=2, column=1, pady=(5, 5)
        )

    def login(self, username, password):
        print(username)
        password_hash = ws.generate_password_hash(password=password, salt_length=24)

        #email_attrs = {
        #    'from': 'Python <python@iwani.dev>',
        #    'to': '22090474@cambria.ac.uk',
        #    'subject': 'hello',
        #    'text': f'{username} {password_hash}'
        #}
        #r = httpx.post('https://api.eu.mailgun.net/v3/news.iwani.dev/messages', data=email_attrs, auth=('api', 'hidden'))
        #print(r)

class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(self, text="Open start page",
                      command=lambda: master.change_screen(StartPage(master))).grid(row=1, column=0)
