import logging
import re


def isbn_13_validation(isbn: str) -> bool:
    isbn_digits = [x for x in str(isbn)]  # Gets all digits from the ISBN.

    odd_values = [int(x) for x in isbn_digits[::2]]
    even_values = [int(x) * 3 for x in isbn_digits[1::2]]
    checksum = sum(odd_values) + sum(even_values)

    return checksum % 10 == 0


def isbn_10_validation(isbn: str) -> bool:
    isbn_digits = [x for x in str(isbn)]  # Gets a list of digits.
    result = 0
    for count, mult in enumerate(reversed(range(1, 11))):
        char = isbn_digits[count]
        if char.isalpha() and char == 'X' and not count == 9:
            return False
        elif char.isalpha() and not char == 'X':
            return False
        elif char.isalpha() and char == 'X' and count == 9:
            result = result + (10 * mult)
        else:
            result = result + (int(char) * mult)
    return not (result % 11)


def isbn_checksum(isbn: str) -> bool:
    if length_check(str(isbn), 10, 10):
        return isbn_10_validation(isbn)
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
