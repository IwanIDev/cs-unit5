import logging
import sqlite3
from datetime import datetime
from typing import List, Tuple
from .book import Book, CopyOfBook
from .author import Author
from .location import Location
from .exceptions import BookDatabaseException, BooksSearchException, LocationDatabaseException
import database as db
from contextlib import closing
from typing import Optional
import pandas as pd


def add_book_to_database(book: Book, database: db.Database) -> Book:
    data = {
        'title': book.title,
        'author': book.author.id,
        'isbn': book.isbn,
        'datePublished': str(book.date_published.timestamp()),
        'genre': book.genre,
        'InfoLink': book.info_link
    }
    sql = """
    INSERT INTO books (Name, AuthorID, ISBN, DatePublished, Genre, InfoLink) VALUES (?, ?, ?, ?, ?, ?)
    RETURNING BookID;
    """
    database_cell = db.DatabaseCell(table='books', data=data)
    with closing(database.connection.cursor()) as cursor:
        try:
            output = cursor.execute(sql,
                                    (data['title'], data['author'], data['isbn'], data['datePublished'], data['genre'], data['InfoLink']))
        except sqlite3.Error as e:
            logging.error(msg=f"Book {book.title} couldn't be add to database, error is {str(e)}.")
            raise BookDatabaseException(str(e))
        output = output.fetchone()
    database.connection.commit()
    book = Book(bookid=output[0], title=data['title'], author=data['author'], isbn=data['isbn'],
                date_of_publishing=book.date_published, genre=data['genre'])
    return book


def get_all_books(database: db.Database) -> List[Book]:
    sql = """
        SELECT Books.BookID, Books.Name, Books.ISBN, Books.DatePublished, Books.Genre, Books.AuthorID, Authors.Name, Books.InfoLink
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
        author = Author(name=book[6], id=book[5])
        books.append(Book(bookid=book[0], title=book[1], isbn=book[2], date_of_publishing=datetime.fromtimestamp(book[3]),
                          genre=book[4], author=author, info_link=book[7]))
    return books


def delete_book(database: db.Database, book: Book) -> bool:
    isbn = str(book.isbn)
    sql = """
    SELECT BookID FROM Books WHERE ISBN = ?;
    """  # This query gets the book's ID.
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (isbn,))
        except sqlite3.Error as e:
            logging.error(msg=f"Couldn't delete book, {str(e)}!")
            return False
        book_id = res.fetchone()[0]  # Gets the ID itself from the result.

    sql = """
    DELETE FROM CopyOfBook WHERE BookID = ?;
    """  # This query deletes every copy of that book.
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (book_id,))
        except sqlite3.Error as e:
            logging.error(msg=f"Couldn't delete book, {str(e)}")
            return False
    database.connection.commit()
    sql = """
    DELETE FROM Books WHERE BookID = ?;
    """  # The book can now finally be deleted.
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (book_id,))
        except sqlite3.Error as e:
            logging.error(msg=f"Couldn't delete book, {str(e)}.")
            return False
    database.connection.commit()
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


def search_book(name: str, authorid: str, database: db.Database) -> List[Book]:
    sql = """
    SELECT Books.BookID, Books.Name, Books.ISBN, Books.DatePublished, Books.Genre, Books.AuthorID, Authors.Name
    FROM Books
    INNER JOIN Authors ON (Books.AuthorID = Authors.AuthorID)
    WHERE Books.Name LIKE ? AND Books.AuthorID LIKE ?;
    """
    values = []
    if name != "":
        values.append(f"%{name}%")
    else:
        values.append("%")
    if authorid != "":
        values.append(authorid)
    else:
        values.append("%")
    values_tuple = tuple(values)

    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, values_tuple)
        except sqlite3.Error as e:
            logging.warning(f"Error in searching books, {e.__class__.__name__}: {str(e)}.")
            raise BooksSearchException(str(e))
        result = res.fetchall()

    if len(result) == 0:
        return []
    return [
        Book(bookid=x[0], title=x[1], isbn=x[2], author=Author(name=x[6], id=x[5]), genre=x[4], date_of_publishing=datetime.fromtimestamp(x[3]))
        for x in result
    ]


def get_author_id(name: str, database: db.Database) -> Author:
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
            return Author(name=name, id=new_author)
        return Author(name=name, id=int(authors[0][0]))


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
        output = res.fetchall()[0]
        if isinstance(output, tuple):
            output = output[0]  # Weird error happening because sometimes this is a tuple?
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
    authorid = str(authors[0][0])
    author = Author(name=authors[0][0], id=author_id)
    return author


def get_all_authors(database: db.Database) -> pd.DataFrame:
    sql = """
    SELECT AuthorID, Name FROM Authors;
    """
    res = pd.read_sql_query(sql, database.connection)
    df = pd.DataFrame(data=res, columns=['AuthorID', 'Name'])
    return df


def add_copy(database: db.Database, book: Book, owner_id: int, location_name: str):
    sql = """
    INSERT INTO CopyOfBook (BookID, OwnerID, LocationID) VALUES (?, ?, ?) RETURNING CopyID;
    """
    location = add_location(database, location_name)
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (book.id, owner_id, location.id))
        except sqlite3.Error as e:
            logging.error(f"Error adding copy of book {book.id}, {e.__class__.__name__}: {str(e)}.")
            return False
        copy = res.fetchone()[0]
        logging.warning(f"Copy of book {book.title} made, {copy}")
    database.connection.commit()
    return CopyOfBook(copy_id=copy, book=book, location=Location(name=location_name), owner_id=owner_id)


def get_copies_from_book(database: db.Database, book: Book):
    sql = """
    SELECT Books.BookID, CopyOfBook.CopyID, CopyOfBook.OwnerID, CopyOfBook.LocationID, Locations.Name FROM CopyOfBook
    INNER JOIN Books ON (CopyOfBook.BookID = Books.BookID)
    INNER JOIN Locations ON (CopyOfBook.LocationID = Locations.LocationID)
    WHERE Books.BookID = ?;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (book.id,))
        except sqlite3.Error as e:
            logging.error(f"Error getting book copies, {e.__class__.__name__}: {str(e)}.")
            raise BookDatabaseException(f"{e.__class__.__name__}: {str(e)}")
        output = res.fetchall()
    return [
        CopyOfBook(copy_id=x[1], owner_id=x[2], book=book, location=Location(id=x[3], name=x[4])) for x in output
    ]


def add_location(database: db.Database, location: str):
    sql = """
    SELECT LocationID, Name FROM Locations WHERE Name = ?;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (location,))
        except sqlite3.Error as e:
            logging.error(f"Error adding location {location}, error {e.__class__.__name__}: {str(e)}.")
            raise LocationDatabaseException(str(e))
        location_found = res.fetchone()
    if location_found is not None:
        return Location(id=location_found[0], name=location_found[1])

    sql = """
    INSERT INTO Locations (Name) VALUES (?) RETURNING LocationID;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql, (location,))
        except sqlite3.Error as e:
            logging.error(f"Error adding location {location}, {e.__class__.__name__}: {str(e)}.")
            raise LocationDatabaseException(str(e))
        id = res.fetchone()
        database.connection.commit()
    return Location(id=id[0], name=location)


def get_locations(database: db.Database) -> List[Location]:
    sql = """
    SELECT LocationID, Name FROM Locations;
    """
    with closing(database.connection.cursor()) as cursor:
        try:
            res = cursor.execute(sql)
        except sqlite3.Error as e:
            logging.error(f"Error getting locations, {e.__class__.__name__}: {str(e)}.")
            raise LocationDatabaseException(f"{e.__class__.__name__}: {str(e)}")
        result = res.fetchall()
    return [
        Location(id=x[0], name=x[1]) for x in result
    ]
