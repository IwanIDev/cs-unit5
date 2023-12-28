from abc import ABC, abstractmethod
import sqlite3
from tkinter import messagebox
from contextlib import closing


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
    def read(self, query):
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

    def create(self, database_cell: DatabaseCell):
        table = database_cell.table
        data = database_cell.data

        # When we construct a DatabaseCell, we take in a dictionary.  This turns that into
        # a list of keys as a string in SQL format and a tuple of values.  A bit annoying, but it works.
        keys = ', '.join([key for key in data])
        values = tuple([*data.values()])

        sql = f"""
        INSERT INTO {table} ({keys}) VALUES(?, ?);
        """ # Constructs the SQL query, but doesn't take the user-generated data yet, to avoid
            # possible SQL injections.

        with closing(self.connection.cursor()) as cursor:
            try:
                cursor.executemany(sql, (values,)) # Even I don't understand why this works tbh.
            except sqlite3.Error as e:
                messagebox.showerror("Database error occured!", f"Database error\n{e}") # Probably a bit vague.
                return

        self.connection.commit()
        messagebox.showinfo("Data entered.", "Data entered into database.") # TODO: Turn this into a debug message.


    def update(self):
        pass  # Insert data into database

    def read(self, query):
        pass  # Query data from database


database = Sqlite3Database(database_url="database.db",
                           tables={
                               "users": ["userid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
                                         "username TEXT NOT NULL",
                                         "password TEXT NOT NULL"],  # Add the rest of the tables here.
                           })
