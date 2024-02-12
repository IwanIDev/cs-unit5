class IsbnInvalidException(Exception):
	def __init__(self, message=""):
		self.message = message
		super().__init__(message)
	def __str__(self):
		return self.message

class BookDatabaseException(Exception):
	def __init__(self, message=""):
		self.message = message
		super().__init__(message)
	def __str__(self):
		return self.message
