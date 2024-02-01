import database as db
from .user import User
from typing import Tuple


def add_user_to_database(database: db.Database, user: User):
    data = {
        "username": user.username,
        "password": user.password,
        "dateCreated": str(user.date_created.timestamp())
    }
    database_cell = db.DatabaseCell(table="users", data=data)
    result = database.create(database_cell=database_cell)
    return result, True
