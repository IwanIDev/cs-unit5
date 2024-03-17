import logging
import re


def isbn_13_validation(isbn: str) -> bool:
    isbn_digits = [x for x in str(isbn)]  # Gets all digits from the ISBN.

    odd_values = [int(x) for x in isbn_digits[::2]]
    even_values = [int(x) * 3 for x in isbn_digits[1::2]]
    checksum = sum(odd_values) + sum(even_values)

    return checksum % 10 == 0


def isbn_checksum(isbn: str) -> bool:
    if length_check(str(isbn), 10, 10):
        return True
    elif length_check(str(isbn), 13, 13):
        return isbn_13_validation(isbn)
    else:
        return False


def length_check(value: str, min_length: int, max_length: int) -> bool:
    length = len(value)
    return (length >= min_length) and (length <= max_length)


def email_check(email: str) -> bool:
    regex_pattern = re.compile(".+\@.+\..+")
    return bool(re.search(regex_pattern, email))
