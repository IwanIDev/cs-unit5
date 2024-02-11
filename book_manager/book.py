from datetime import datetime


class Book:
    def __init__(self, isbn, title, author, date_of_publishing: datetime):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.date_published: datetime = date_of_publishing
    