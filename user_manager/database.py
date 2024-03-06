import logging
import sqlite3
from contextlib import closing
from typing import Tuple
import database as db
from .user import User
from .exceptions import UserDatabaseErrorException


def add_user_to_database(database: db.Database, user: User) -> bool:
    data = {
        "username": user.username,
        "password": user.password,
        "dateCreated": str(user.date_created.timestamp())
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    try:
        database.create(database_cell=database_cell)
    except db.DatabaseException as e:
        raise UserDatabaseErrorException(str(e))
    return True


def edit_user(database: db.Database, user: User, current_username: str) -> bool:
    data = {
        "username": user.username,
        "password": user.password,
        "current_username": current_username
    }
    sql = """
    UPDATE Users SET Username=?, Password=?
    WHERE Username=?;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql,
                                 (data['username'], data['password'], data['current_username'],))
        except sqlite3.Error as e:
            logging.error(msg=f"Error editing user {user.username} in database, {e}.")
            raise UserDatabaseErrorException(str(e))
    database.connection.commit()
    logging.info(msg=f"Successfully updated user {user.username}.")
    return True
