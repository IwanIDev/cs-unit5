from .query import Query
from utils import get_platform_dir
from .AbstractDatabase import Database
from .DatabaseCell import DatabaseCell
from .SqliteDatabase import Sqlite3Database
from .exceptions import *
from pathlib import Path

path = Path(__file__).parent.resolve() / "init.sql"
database = Sqlite3Database(database_url=str(get_platform_dir() / "database.sqlite"), script=path)
