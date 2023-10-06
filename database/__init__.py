from abc import ABC, abstractmethod
import sqlite3


class Database(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read(self, query):
        pass


class Sqlite3Database(Database):
    def __init__(self):
        self.connection = sqlite3.connect("database.db")

    def update(self):
        pass  # Insert data into database

    def read(self, query):
        pass  # Query data from database
