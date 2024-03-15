import re
import logging


def isbn_13_validation(isbn: str) -> bool:
    # From https://stackoverflow.com/questions/38111620/python-isbn-13-digit-validate
    d = re.findall(r'\d', isbn)  # Gets all digits from the ISBN.
    logging.warning(d)
    if len(d) != 13:
        return False

    # The ISBN-13 check digit, which is the last digit of the ISBN, must range from 0 to 9
    # and must be such that the sum of all the thirteen digits, each multiplied by its
    # (integer) weight, alternating between 1 and 3, is a multiple of 10.
    odd = [int(x) for x in d[::2]]
    even = [int(x) * 3 for x in d[1::2]]
    checksum = sum(odd) + sum(even)
    logging.warning(f"odd: {odd}, even: {even}, checksum: {checksum % 10}")
    logging.warning(f"{checksum % 10 == 0}")
    return checksum % 10 == 0


def isbn_10_validation(isbn: str) -> bool:
    # Modified version of https://stackoverflow.com/questions/68587793/making-isbn-10-identifier-in-python
    isbn_digits = [x for x in str(isbn)]
    result = 0
    for index, multiplier in enumerate(reversed(range(1, 11))):
        char = isbn_digits[index]
        if char.isalpha() and char == 'X' and not index == 9:
            return False
        elif char.isalpha() and not char == 'X':
            return False
        elif char.isalpha() and char == 'X' and index == 9:
            result = result + (10 * multiplier)
        else:
            result = result + (int(char) * multiplier)
    return not (result % 11)


def isbn_checksum(isbn: str) -> bool:
    if length_check(str(isbn), 10, 10):
        return isbn_10_validation(isbn)
    if length_check(str(isbn), 13, 13):
        return isbn_13_validation(isbn)


def length_check(value: str, min_length: int, max_length: int) -> bool:
    length = len(value)
    if length < min_length:
        return False
    elif length > max_length:
        return False
    return True


def email_check(email: str) -> bool:
    regex_pattern = re.compile(".+\@.+\..+")
    return bool(re.search(regex_pattern, email))
