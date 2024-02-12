from typing import Dict


class DatabaseCell:
    def __init__(self, table, data: Dict):
        self.table = table
        self.data = data
