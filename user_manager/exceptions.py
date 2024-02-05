class RegisterUserException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class LoginUserException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class UserDatabaseErrorException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
