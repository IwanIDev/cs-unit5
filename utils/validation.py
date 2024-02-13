def isbn_check_digit(isbn: int) -> bool:
    digits = [int(x) for x in str(isbn)]
    lastDigit = digits.pop()
    newDigits = []
    for count, digit in enumerate(digits):
        place = count + 1
        if place % 2 == 0:
            newDigits.append(digit * 3)
        else:
            newDigits.append(digit)
    total = 0
    for digit in newDigits:
        total = total + digit
    modulo = total % 10
    checkDigit = modulo if modulo == 0 else 10 - modulo
    return lastDigit == checkDigit
