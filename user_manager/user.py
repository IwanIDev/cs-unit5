import datetime as dt


class User:
    def __init__(self, username, password, date_created: dt.datetime):
        self.username = username
        self.password = password
        self.date_created = date_created
