import logging
from datetime import datetime
from typing import List, Tuple
from .book import Book
from .exceptions import BookDatabaseException
import database as db


def add_book_to_database(book: Book, database: db.Database) -> bool:
    data = {
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'datePublished': str(book.date_published.timestamp())
    }
    database_cell = db.DatabaseCell(table='books', data=data)
    try:
        result = database.create(database_cell=database_cell)
    except db.DatabaseException as e:
        logging.error(msg=f"Book {book.title} couldn't be add to database, error is {str(e)}.")
        raise BookDatabaseException(str(e))
    return True


def get_all_books(database: db.Database) -> Tuple[List[Book], bool]:
    database_cell = db.DatabaseCell(table='books', data={})
    try:
        result = database.read(database_cell=database_cell)
    except db.DatabaseException as e:
        logging.error(msg=f"Error reading books from database, {e}.")
        return [], False
    logging.info(msg=f"Successfully read books from database.")
    books = []
    for book in result:
        books.append(Book(title=book[1], author=book[2], isbn=book[3], date_of_publishing=datetime.fromtimestamp(book[4])))
    return books, True


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
