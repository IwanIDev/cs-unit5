from pathlib import Path
from .query import Query
from utils import get_platform_dir
from .AbstractDatabase import Database
from .DatabaseCell import DatabaseCell
from .SqliteDatabase import Sqlite3Database
from .exceptions import *


database = Sqlite3Database(database_url=str(Path(__file__).parent.parent.resolve() / "database.sqlite"))
