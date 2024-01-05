import werkzeug.security as ws
import database as db
from typing import Optional


def register_user(database: db.Database, username, password) -> Optional[str]:
    password = ws.generate_password_hash(password=password)
    data = {
        "username": username,
        "password": password
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.create(database_cell=database_cell)
    if isinstance(result, str):
        return result
    return


def login_user(database: db.Database, username: str, password: str) -> tuple:
    data = {
        "username": username
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.read(database_cell)
    if isinstance(result, str):
        return result, False
    return result, True
