from abc import ABC, abstractmethod
from .DatabaseCell import DatabaseCell
from typing import Tuple


class Database(ABC):
    @abstractmethod
    def create(self, database_cell: DatabaseCell):
        pass

    @abstractmethod
    def update(self, database_cell: DatabaseCell, where: Tuple[str, str]):
        pass

    @abstractmethod
    def read(self, database_cell: DatabaseCell):
        pass

    @abstractmethod
    def delete(self, database_cell: DatabaseCell):
        pass

    @abstractmethod
    def backup(self):
        pass

    @abstractmethod
    def restore_from_backup(self, backup: str):
        pass
