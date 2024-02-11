from .query import Query
from utils import get_platform_dir
from .AbstractDatabase import Database
from .DatabaseCell import DatabaseCell
from .SqliteDatabase import Sqlite3Database
from .exceptions import *


database = Sqlite3Database(database_url=str(get_platform_dir() / "database.sqlite"),
                           tables={
                               "users": ["userid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                         "username TEXT NOT NULL UNIQUE",
                                         "password TEXT NOT NULL",
                                         "dateCreated INTEGER NOT NULL"],
                               "books": [
                                   "bookid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                   "title TEXT NOT NULL UNIQUE",
                                   "author TEXT NOT NULL",
                                   "isbn TEXT NOT NULL",
                                   "datePublished INTEGER NOT NULL"
                               ]# Add the rest of the tables here.
                           })
