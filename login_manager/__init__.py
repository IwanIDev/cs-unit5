import werkzeug.security as ws
import database as db
from typing import Optional
import logging


def register_user(database: db.Database, username, password) -> Optional[str]:
    if not username or not password:
        return "No items input."
    password = ws.generate_password_hash(password=password)
    data = {
        "username": username,
        "password": password
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.create(database_cell=database_cell)
    if isinstance(result, int):
        if result == 2067:
            return "Username already exists."
        return str(result)
    logging.info(msg=f"Registered user: {username}.")
    return


def login_user(database: db.Database, username: str, password: str) -> tuple:
    if not username or not password:
        return "Missing data items.", False
    data = {
        "username": username
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.read(database_cell)

    if isinstance(result, str):
        logging.error(msg=f"Failed to login user {username}, database error: {result}.")
        return result, False
    if not result:
        logging.error(msg=f"Failed to login user {username}, no user found.")
        return "User not found", False

    result_cell: tuple = result[0]
    if not ws.check_password_hash(result_cell[2], password):
        logging.error(msg=f"Failed to login user {username}, password incorrect.")
        return "Wrong password", False
    logging.info(msg=f"Logged in successfully as user {result_cell[0]}.")
    return result, True
