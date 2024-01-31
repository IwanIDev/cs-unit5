import logging
from typing import List

from .book import Book
from database import DatabaseCell, database


def add_book_to_database(book: Book) -> bool:
    data = {
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'datePublished': book.date_published
    }
    database_cell = DatabaseCell(table='books', data=data)
    result = database.create(database_cell=database_cell)
    if result is not None:
        logging.error(msg=f"Book {book.title} couldn't be add to database, error is {result}.")
        return False
    return True

def get_all_books() -> List[Book]:
    pass
