from abc import ABC, abstractmethod
import sqlite3


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

    def create_tables(self):
        cursor = self.connection.cursor()
        for table, data in self.tables:
            table_schema = "("
            for column in data:
                table_schema += f" {column}, "
            table_schema += ")"
            cursor.execute(f"""
            
            """)


    def create(self, database_cell: DatabaseCell):
        cursor = self.connection.cursor()
        table = database_cell.table
        data = database_cell.data
        cursor.executemany(f"""
        INSERT INTO {table} VALUES(?, ?, ?)
        """, data)
        self.connection.commit()

    def update(self):
        pass  # Insert data into database

    def read(self, query):
        pass  # Query data from database
