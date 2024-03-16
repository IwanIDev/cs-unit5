import sqlite3
from contextlib import closing
from datetime import datetime
from .user import User, UserType
import database as db
import logging
from typing import Tuple, List


def get_all_users(database: db.Database) -> Tuple[List[User], bool]:
    database_cell = db.DatabaseCell(table='users', data={})
    result = database.read(database_cell=database_cell)
    if isinstance(result, str):
        logging.error(msg=f"Error reading books from database, {result}.")
        return [], False
    logging.info(msg=f"Successfully read books from database.")
    users = []
    for user in result:
        users.append(
            User(user_id=user[0], username=user[1], password=user[2], date_created=datetime.fromtimestamp(user[3]),
                 user_type=UserType(user[4])))
    return users, True


def delete_user(database: db.Database, user: User) -> bool:
    userid = str(user.user_id)
    sql = """
        DELETE FROM CopyOfBook WHERE OwnerID = ?;
        """  # This query deletes every copy of that book.
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (userid,))
        except sqlite3.Error as e:
            logging.error(msg=f"Couldn't delete user, {str(e)}")
            return False
    database.connection.commit()
    sql = """
        DELETE FROM Users WHERE UserID = ?;
        """  # The book can now finally be deleted.
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (userid,))
        except sqlite3.Error as e:
            logging.error(msg=f"Couldn't delete user, {str(e)}.")
            return False
    database.connection.commit()
    return True


def edit_user(database: db.Database, user: User) -> Tuple[str, bool]:
    data = {
        "username": user.username,
        "password": user.password,
        "dateCreated": str(user.date_created.timestamp())
    }
    where = ("username", user.username)
    database_cell = db.DatabaseCell(table="users", data=data)
    logging.info(msg=f"{database_cell.table}, {str(database_cell.data)}")
    result = database.update(database_cell=database_cell, where=where)
    if isinstance(result, str):
        logging.error(msg=f"Database error: {result}.")
        return result, False
    logging.info(msg=f"Successfully updated user {user.username}.")
    return "", True
