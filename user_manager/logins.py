import sqlite3
from contextlib import closing
import werkzeug.security as ws
import database as db
import logging
from utils import length_check
from .user import User, UserType
from .database import add_user_to_database
from .exceptions import RegisterUserException, LoginUserException, UserDatabaseErrorException
from datetime import datetime


def register_user(database: db.Database, username, password) -> bool:
    if not username or not password:
        raise RegisterUserException("Both fields must be filled.")
    username_valid = length_check(username, 4, 32)
    password_valid = length_check(password, 2, 64)

    error = ""
    if not username_valid:
        error += "Usernames must have at least 4 characters and at most 32."
    if not password_valid:
        error += "Passwords must have at least 2 and at most 64 characters."
    if error != "":
        raise RegisterUserException(error)

    num_of_users_sql = """
    SELECT COUNT(UserID) FROM Users;
    """
    count = 0
    try:
        with closing(database.connection.cursor()) as cursor:
            res = cursor.execute(num_of_users_sql)
            count = res.fetchall()[0][0]
    except sqlite3.Error as e:
        logging.error(f"Error getting count of users, {str(e)}")
        count = 1
    if count <= 0:
        logging.info("First user registered, making type admin.")
        user_type = UserType.ADMIN
    else:
        user_type = UserType.USER

    user_to_register = User(username=username, password=ws.generate_password_hash(password), date_created=datetime.now(), user_type=user_type)

    try:
        result = add_user_to_database(database, user_to_register)
    except UserDatabaseErrorException as e:
        if "UNIQUE constraint failed" in str(e):
            raise RegisterUserException("Username already exists.")
        raise RegisterUserException(str(e))
    logging.info(msg=f"Registered user: {username}.")
    return True


def login_user(database: db.Database, username: str, password: str) -> User:
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
    user = User(user_id=result_cell[0], username=result_cell[1], password=result_cell[2], date_created=datetime.fromtimestamp(result_cell[3]), user_type=UserType(result_cell[4]))
    return user
