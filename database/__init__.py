from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read(self, query):
        pass


class Sqlite3Database(Database):
    def __init__(self):
        pass  # Create database

    def update(self):
        pass  # Insert data into database

    def read(self, query):
        pass  # Query data from database
