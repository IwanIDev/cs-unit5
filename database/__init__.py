from abc import ABC, abstractmethod
import sqlite3
from tkinter import messagebox
from contextlib import closing
from .query import Query
from typing import Optional
import logging


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

        sql = f"""
        INSERT INTO {table} ({keys}) VALUES(?, ?);
        """  # Constructs the SQL query, but doesn't take the user-generated data yet, to avoid
        # possible SQL injections.

        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.executemany(sql, (values,))  # Even I don't understand why this works tbh.
            except sqlite3.Error as e:
                return e.sqlite_errorcode

        self.connection.commit()
        logging.log(logging.INFO, f"Created data {data} in table {table}.")
        return

    def update(self):
        pass  # Insert data into database

    def read(self, database_cell: DatabaseCell):
        table = database_cell.table
        data = database_cell.data

        keys = ', '.join([key for key in data])
        value = str(list(data.values())[0])
        logging.log(logging.INFO, f"{value}")

        sql = f"""
        SELECT * FROM {table} WHERE {keys} LIKE ?;
        """

        with closing(self.connection.cursor()) as cursor:
            try:
                res = cursor.execute(sql, (value,))
            except sqlite3.Error as e:
                return str(e)
            logging.log(logging.INFO, f"Queried data {data} from table {table}.")
            return res.fetchall()


database = Sqlite3Database(database_url="database.db",
                           tables={
                               "users": ["userid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                         "username TEXT NOT NULL UNIQUE",
                                         "password TEXT NOT NULL"],  # Add the rest of the tables here.
                           })
