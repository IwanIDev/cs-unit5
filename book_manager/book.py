from datetime import datetime
from .location import Location
from .author import Author
from dataclasses import dataclass, field


class Book:
    def __init__(self, isbn, title, author: Author, date_of_publishing: datetime, genre, bookid=0, info_link=""):
        self.id = bookid
        self.isbn = isbn
        self.title = title
        self.author = author
        self.date_published: datetime = date_of_publishing
        self.genre = genre
        self.info_link = info_link

    def __str__(self):
        return f"{self.title}, {self.isbn}, {self.author}, {self.date_published}, {self.genre}"


@dataclass
class CopyOfBook:
    book: Book
    location: Location
    owner_id: int
    copy_id: int = field(default=0)
