from datetime import datetime

from .user import User
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
        users.append(User(username=user[1], password=user[2], date_created=datetime.fromtimestamp(user[3])))
    return users, True


def delete_user(database: db.Database, user: User) -> bool:
    data = {
        "username": user.username
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.delete(database_cell=database_cell)
    if isinstance(result, str):
        logging.error(msg=f"Couldn't delete from database, {result}")
        return False
    logging.info(msg=f"Successfully deleted {user.username} from database.")
    return True


def edit_book(database: db.Database, user: User) -> Tuple[str, bool]:
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

