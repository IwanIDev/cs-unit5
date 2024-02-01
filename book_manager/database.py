import logging
from datetime import datetime
from typing import List, Tuple
from .book import Book
import database as db


def add_book_to_database(book: Book, database: db.Database) -> bool:
    data = {
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'datePublished': book.date_published.timestamp()
    }
    database_cell = db.DatabaseCell(table='books', data=data)
    result = database.create(database_cell=database_cell)
    if result is not None:
        logging.error(msg=f"Book {book.title} couldn't be add to database, error is {result}.")
        return False
    return True


def get_all_books(database: db.Database) -> Tuple[List[Book], bool]:
    database_cell = db.DatabaseCell(table='books', data={})
    result = database.read(database_cell=database_cell)
    if isinstance(result, str):
        logging.error(msg=f"Error reading books from database, {result}.")
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
    result = database.delete(database_cell=database_cell)
    if isinstance(result, str):
        logging.error(msg=f"Couldn't delete from database, {result}")
        return False
    logging.info(msg=f"Successfully deleted {book.title} from database.")
    return True
