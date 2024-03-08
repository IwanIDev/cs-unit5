import logging
import sqlite3
from datetime import datetime
from typing import List, Tuple
from .book import Book
from .exceptions import BookDatabaseException
import database as db
from contextlib import closing
from typing import Optional
import pandas as pd


def add_book_to_database(book: Book, database: db.Database) -> Book:
    data = {
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'datePublished': str(book.date_published.timestamp()),
        'genre': book.genre
    }
    sql = """
    INSERT INTO books (Name, AuthorID, ISBN, DatePublished, Genre) VALUES (?, ?, ?, ?, ?)
    RETURNING BookID;
    """
    database_cell = db.DatabaseCell(table='books', data=data)
    with closing(database.connection.cursor()) as cursor:
        try:
            output = cursor.execute(sql,
                                    (data['title'], data['author'], data['isbn'], data['datePublished'], data['genre']))
        except sqlite3.Error as e:
            logging.error(msg=f"Book {book.title} couldn't be add to database, error is {str(e)}.")
            raise BookDatabaseException(str(e))
        output = output.fetchone()
    database.connection.commit()
    book = Book(bookid=output[0], title=data['title'], author=data['author'], isbn=data['isbn'],
                date_of_publishing=book.date_published, genre=data['genre'])
    return book


def get_all_books(database: db.Database) -> Tuple[List[Book], bool]:
    with closing(database.connection.cursor()) as cursor:
        try:
            output = cursor.execute("""
            SELECT Name, AuthorID, ISBN, DatePublished, Genre FROM Books;
            """)
            result = output.fetchall()
        except sqlite3.Error as e:
            logging.error(msg=f"Error reading books from database, {e}.")
            return [], False
    logging.info(msg=f"Successfully read books from database.")
    books = []
    for book in result:
        logging.warning(f"Book {book[0]}: {book}")
        books.append(
            Book(title=book[0], author=book[1], isbn=book[2], date_of_publishing=datetime.fromtimestamp(book[3]),
                 genre=book[4]))
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
        "datePublished": str(book.date_published.timestamp()),
        "genre": book.genre
    }
    logging.warning(str(book.author))
    sql = """
    UPDATE Books SET Name=?, ISBN=?, AuthorID=?, DatePublished=?, Genre=?
    WHERE ISBN=?;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql,
                                 (data['title'], data['isbn'], data['author'], data['datePublished'], data['genre'], data['isbn']))
        except sqlite3.Error as e:
            logging.error(msg=f"Error editing book {book.title} in database, {e}.")
            return str(e), False
    database.connection.commit()
    logging.info(msg=f"Successfully updated book {book.title}.")
    return "", True


def get_book_id(name: str, database: db.Database) -> int:
    sql = """
    SELECT BookID FROM Books WHERE Name = ?;
    """
    with closing(database.connection.cursor()) as cursor:
        res = cursor.execute(sql, (name,))
        books = res.fetchall()
        if len(books) <= 0:
            return 0
    return int(books[0][0])


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
    INSERT INTO Authors (Name) VALUES (?);
    """
    output = 0
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (name,))
        except sqlite3.Error as e:
            logging.error(f"Error adding author {name}, error {e}.")
            return None
        output = cursor.lastrowid
    database.connection.commit()
    return output


def get_author_from_id(author_id: int, database: db.Database) -> Optional[str]:
    sql = """
    SELECT Name FROM Authors WHERE AuthorID = ?;
    """
    authors = []
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (author_id,))
        except sqlite3.Error as e:
            logging.error(f"Error getting author {author_id}, error {e}.")
            return None
        authors = res.fetchall()
    if len(authors) <= 0:
        return None
    author = authors[0][0]
    return author


def get_all_authors(database: db.Database) -> pd.DataFrame:
    sql = """
    SELECT AuthorID, Name FROM Authors;
    """
    res = pd.read_sql_query(sql, database.connection)
    df = pd.DataFrame(data=res, columns=['AuthorID', 'Name'])
    return df


def add_copy(database: db.Database, book_id: int, owner_id: int):
    sql = """
    INSERT INTO CopyOfBook (BookID, OwnerID) VALUES (?, ?) RETURNING CopyID;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (book_id, owner_id))
        except sqlite3.Error as e:
            logging.error(f"Error adding copy of book {book_id}, error {str(e)}.")
            return False
        copyid = res.fetchone()[0]
        logging.warning(f"Copy of book {book_id} made, {copyid}")
    database.connection.commit()
    return True
