import datetime as dt
import enum


class UserType(enum.IntEnum):
    ADMIN = 0
    USER = 1


class User:
    def __init__(self, username, password, date_created: dt.datetime, user_type: UserType = UserType.USER,
                 user_id: int = 0):
        self.username = username
        self.password = password
        self.date_created = date_created
        self.user_type = user_type
        self.user_id = user_id
