import werkzeug.security as ws
import database as db


def register_user(database: db.Database, username, password):
    password = ws.generate_password_hash(password=password)
    data = [
        ("username", username),
        ("password", password),
    ]
    database_cell = db.DatabaseCell(table="users", data=data)
    database.create(database_cell=database_cell)
    return
