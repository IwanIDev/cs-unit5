import werkzeug.security as ws
import database as db
from typing import Tuple
import logging
from .user import User
from .database import add_user_to_database
from datetime import datetime


def register_user(database: db.Database, username, password) -> Tuple[str, bool]:
    if not username or not password:
        return "No items input.", False
    user_to_register = User(username=username, password=password, date_created=datetime.now())
    result = add_user_to_database(database, user_to_register)
    if result is not None:
        if "UNIQUE constraint failed" in str(result):
            return "Username already exists.", False
        return str(result), False
    logging.info(msg=f"Registered user: {username}.")
    return "", True


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
