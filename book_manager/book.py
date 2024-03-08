from datetime import datetime


class Book:
    def __init__(self, isbn, title, author, date_of_publishing: datetime, genre, bookid=0):
        self.id = bookid
        self.isbn = isbn
        self.title = title
        self.author = author
        self.date_published: datetime = date_of_publishing
        self.genre = genre

    def __str__(self):
        return f"{self.title}, {self.isbn}, {self.author}, {self.date_published}, {self.genre}"
