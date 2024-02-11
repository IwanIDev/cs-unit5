from .DatabaseCell import DatabaseCell
from .AbstractDatabase import Database
from .exceptions import DatabaseException, DatabaseNoDataUpdatedException
import sqlite3
from typing import Optional, Tuple, List
import logging
from contextlib import closing


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

    def create(self, database_cell: DatabaseCell) -> bool:
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
                logging.error(msg=f"Database error: {e}, message: {str(e)}")
                raise DatabaseException(str(e))

        self.connection.commit()
        return True

    def update(self, database_cell: DatabaseCell, where: Tuple[str, str]) -> bool:
        table = database_cell.table
        data = database_cell.data
        keys = list(data.keys())
        values = tuple([*data.values()])
        set_statement = []
        for key, value in data.items():
            set_statement.append(f"{key} = ?")
        set_string = ', '.join(set_statement)
        where_string = f"'{where[1]}'" if type(where[1]) is str else str(where[1])
        where_statement = f"{where[0]} = {where_string}"
        sql = f"""
        UPDATE {table} SET {set_string} WHERE {where_statement};
        """

        with closing(self.connection.cursor()) as cursor:
            try:
                res = cursor.executemany(sql, (values,))
            except sqlite3.Error as e:
                raise DatabaseException(str(e))
            if cursor.rowcount <= 0:
                logging.info(msg=f"Row count failed.")
                raise DatabaseNoDataUpdatedException("Rows updated 0, no data updated.")
        self.connection.commit()
        return True

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
                    res = cursor.execute(sql, (value,))
                else:
                    res = cursor.execute(sql)
            except sqlite3.Error as e:
                raise DatabaseException(str(e))
        self.connection.commit()
        return

    def read(self, database_cell: DatabaseCell) -> List[Tuple]:
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


        with closing(self.connection.cursor()) as cursor:
            try:
                if value:
                    res = cursor.execute(sql, (value,))
                else:
                    res = cursor.execute(sql)
            except sqlite3.Error as e:
                raise DatabaseException(str(e))
            return res.fetchall()
