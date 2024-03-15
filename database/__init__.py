from .query import Query
from utils import get_platform_dir
from .AbstractDatabase import Database
from .DatabaseCell import DatabaseCell
from .SqliteDatabase import Sqlite3Database
from .exceptions import *
from pathlib import Path
import logging

script_path = Path(__file__).parent.resolve() / "init.sql"
database_path = Path(__file__).parent.parent.resolve() / "database.sqlite"
logging.warning(f"Loading {str(database_path)}")
database = Sqlite3Database(database_url=str(database_path), script=script_path)
