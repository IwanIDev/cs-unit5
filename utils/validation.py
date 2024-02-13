import re

def isbn_checksum(isbn: int) -> bool:
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
