import werkzeug.security as ws
import datetime as dt


class User:
    def __init__(self, username, password, date_created: dt.datetime):
        self.username = username
        self.password = ws.generate_password_hash(password=password)
        self.date_created = date_created
