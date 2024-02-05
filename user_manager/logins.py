import werkzeug.security as ws
import database as db
import logging
from .user import User
from .database import add_user_to_database
from .exceptions import RegisterUserException, LoginUserException, UserDatabaseErrorException
from datetime import datetime


def register_user(database: db.Database, username, password) -> bool:
    if not username or not password:
        raise RegisterUserException("Both fields must be filled.")
    user_to_register = User(username=username, password=password, date_created=datetime.now())
    try:
        result = add_user_to_database(database, user_to_register)
    except UserDatabaseErrorException as e:
        if "UNIQUE constraint failed" in str(e):
            raise RegisterUserException("Username already exists.")
        raise RegisterUserException(str(e))
    logging.info(msg=f"Registered user: {username}.")
    return True


def login_user(database: db.Database, username: str, password: str) -> bool:
    if not username or not password:
        raise LoginUserException("Both fields must be filled.")
    data = {
        "username": username
    }
    database_cell = db.DatabaseCell(table="users", data=data)

    try:
        result = database.read(database_cell)
    except db.DatabaseException as e:
        logging.error(msg=f"Failed to login user {username}, database error: {str(e)}.")
        raise LoginUserException(str(e))

    if not result:
        logging.error(msg=f"Failed to login user {username}, no user found.")
        raise LoginUserException("Login failed, username or password incorrect.")

    result_cell: tuple = result[0]
    if not ws.check_password_hash(result_cell[2], password):
        logging.error(msg=f"Failed to login user {username}, password incorrect.")
        raise LoginUserException("Login failed, username or password incorrect.")

    logging.info(msg=f"Logged in successfully as user {result_cell[0]}.")
    return True
