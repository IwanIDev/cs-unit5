import logging
import sqlite3
from contextlib import closing
from datetime import datetime
from typing import List, Tuple, Optional
from .book import Book
from .exceptions import BookDatabaseException
import database as db


def add_book_to_database(book: Book, database: db.Database) -> bool:
    author_id = get_author_id(book.author, database)
    data = {
        'name': book.title,
        'authorid': author_id,
        'isbn': book.isbn,
        'datePublished': str(book.date_published.timestamp()),
        'genre': ""
    }
    database_cell = db.DatabaseCell(table='books', data=data)
    try:
        result = database.create(database_cell=database_cell)
    except db.DatabaseException as e:
        logging.error(msg=f"Book {book.title} couldn't be add to database, error is {str(e)}.")
        raise BookDatabaseException(str(e))
    return True


def get_all_books(database: db.Database) -> List[Book]:
    sql = """
    SELECT Books.Name, Books.ISBN, Books.DatePublished, Books.Genre, Books.AuthorID, Authors.Name
    FROM Books
    INNER JOIN Authors ON (Books.AuthorID = Authors.AuthorID)
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            result = cursor.execute(sql)
        except sqlite3.Error as e:
            logging.error(msg=f"Error reading books from database, {e}.")
            raise BookDatabaseException(str(e))
        data = result.fetchall()
    logging.info(msg=f"Successfully read books from database.")
    books = []
    for book in data:
        books.append(Book(title=book[0], isbn=book[1], date_of_publishing=datetime.fromtimestamp(book[2]),
                          author=book[5]))
    return books


def delete_book(database: db.Database, book: Book) -> bool:
    data = {
        "isbn": book.isbn
    }
    database_cell = db.DatabaseCell(table="books", data=data)
    try:
        result = database.delete(database_cell=database_cell)
    except db.DatabaseException as e:
        logging.error(msg=f"Couldn't delete from database, {result}")
        return False
    logging.info(msg=f"Successfully deleted {book.title} from database.")
    return True


def edit_book(database: db.Database, book: Book) -> Tuple[str, bool]:
    data = {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "datePublished": str(book.date_published.timestamp())
    }
    where = ("isbn", str(book.isbn))
    database_cell = db.DatabaseCell(table="books", data=data)
    try:
        result = database.update(database_cell=database_cell, where=where)
    except db.DatabaseNoDataUpdatedException as e:
        logging.error(msg=f"Database error, no data was updated, {str(e)}")
        return str(e), False
    except db.DatabaseException as e:
        logging.error(msg=f"Database error, {str(e)}")
        return str(e), False
    logging.info(msg=f"Successfully updated book {book.title}.")
    return "", True


def get_author_id(name: str, database: db.Database) -> int:
    sql = """
    SELECT AuthorID FROM Authors WHERE Name = ?;
    """
    with closing(database.connection.cursor()) as cursor:
        res = cursor.execute(sql, (name,))
        authors = res.fetchall()
        if len(authors) <= 0:
            new_author = add_author(name, database)
            if new_author is None:
                return 0
            return new_author
        return int(authors[0][0])


def add_author(name: str, database: db.Database) -> Optional[int]:
    sql = """
    INSERT INTO Authors (Name) VALUES (?)
    RETURNING AuthorID;
    """
    output = 0
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (name,))
        except sqlite3.Error as e:
            logging.error(f"Error adding author {name}, error {e}.")
            return None
        output = res.fetchone()[0]
    database.connection.commit()
    return output
