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
        cursor = self.connection.cursor()
        table = database_cell.table
        data = database_cell.data

        keys = [i[0] for i in data]
        values = (i[1] for i in data)
        keys = ', '.join(keys)
        print(keys, values)

        sql = f"""
        INSERT INTO {table} ({keys}) VALUES(?, ?);
        """
        print(sql)
        cursor.executemany(sql, values)
        self.connection.commit()

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
