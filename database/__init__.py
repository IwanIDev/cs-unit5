from abc import ABC, abstractmethod
import sqlite3
from contextlib import closing
from .query import Query
from typing import Optional
import logging
from utils import get_platform_dir


class DatabaseCell:
    def __init__(self, table, data):
        self.table = table
        self.data = data


class Database(ABC):
    @abstractmethod
    def create(self, database_cell: DatabaseCell):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read(self, database_cell: DatabaseCell):
        pass

    @abstractmethod
    def delete(self, database_cell: DatabaseCell):
        pass


class Sqlite3Database(Database):
    def __init__(self, database_url, tables):
        self.connection = sqlite3.connect(database_url)
        self.tables = tables
        self.create_tables(tables)

    def create_tables(self, tables):
        cursor = self.connection.cursor()
        for table, data in tables.items():
            table_schema = "("
            table_schema += ', '.join(data)
            table_schema += ")"
            print(table_schema)
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table}{table_schema};
            """)
        self.connection.commit()
        return

    def create(self, database_cell: DatabaseCell) -> Optional[int]:
        table = database_cell.table
        data = database_cell.data

        # When we construct a DatabaseCell, we take in a dictionary.  This turns that into
        # a list of keys as a string in SQL format and a tuple of values.  A bit annoying, but it works.
        keys = ', '.join([key for key in data])
        values = tuple([*data.values()])

        qmark = "?"
        for cols in range(1, len(values)):
            qmark += ",?"

        sql = f"""
        INSERT INTO {table} ({keys}) VALUES({qmark});
        """  # Constructs the SQL query, but doesn't take the user-generated data yet, to avoid
        # possible SQL injections.

        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.executemany(sql, (values,))  # Even I don't understand why this works tbh.
            except sqlite3.Error as e:
                logging.error(msg=f"Database error: {e.sqlite_errorcode}, message: {str(e)}")
                return e.sqlite_errorcode

        self.connection.commit()
        logging.log(logging.INFO, f"Created data {data} in table {table}.")
        return

    def update(self):
        pass  # Insert data into database

    def delete(self, database_cell: DatabaseCell) -> Optional[str]:
        table = database_cell.table
        data = database_cell.data
        keys = ', '.join([key for key in data])
        sql = ""
        if len(data) < 1:
            sql = f"""
                           DELETE FROM {table};
                           """
            value = ""
        else:
            sql = f"""
                           DELETE FROM {table} WHERE {keys} LIKE ?;
                           """
            value = str(list(data.values())[0])

        with closing(self.connection.cursor()) as cursor:
            try:
                if value:
                    logging.info(msg=f"{value}")
                    res = cursor.execute(sql, (value,))
                else:
                    res = cursor.execute(sql)
            except sqlite3.Error as e:
                return str(e)
            logging.log(logging.INFO, f"Deleted data {data} from table {table}.")
        self.connection.commit()
        return

    def read(self, database_cell: DatabaseCell):
        table = database_cell.table
        data = database_cell.data

        keys = ', '.join([key for key in data])
        sql = ""
        if len(data) < 1:
            sql = f"""
                   SELECT * FROM {table};
                   """
            value = ""
        else:
            sql = f"""
                   SELECT * FROM {table} WHERE {keys} LIKE ?;
                   """
            value = str(list(data.values())[0])

        logging.log(logging.INFO, f"{value}")

        with closing(self.connection.cursor()) as cursor:
            try:
                if value:
                    res = cursor.execute(sql, (value,))
                else:
                    res = cursor.execute(sql)
            except sqlite3.Error as e:
                return str(e)
            logging.log(logging.INFO, f"Queried data {data} from table {table}.")
            return res.fetchall()


database = Sqlite3Database(database_url=str(get_platform_dir() / "database.sqlite"),
                           tables={
                               "users": ["userid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                         "username TEXT NOT NULL UNIQUE",
                                         "password TEXT NOT NULL",
                                         "dateCreated INTEGER NOT NULL"],
                               "books": [
                                   "bookid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                   "title TEXT NOT NULL",
                                   "author TEXT NOT NULL",
                                   "isbn TEXT NOT NULL",
                                   "datePublished INTEGER NOT NULL"
                               ]# Add the rest of the tables here.
                           })
