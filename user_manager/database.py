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
