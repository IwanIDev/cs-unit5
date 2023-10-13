from ui import App
import customtkinter
import database as db

if __name__ == '__main__':
    customtkinter.set_default_color_theme("green")

    database = db.Sqlite3Database(database_url="database.db",
                                  tables={
                                      "users": ["userid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                                "username TEXT NOT NULL",
                                                "password TEXT NOT NULL"],  # Add the rest of the tables here.
                                    })

    app = App()
    app.mainloop()
