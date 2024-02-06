import httpx
from book_manager import Book
from typing import Tuple, Optional
import json
import logging
from datetime import datetime
from utils import isbn_check_digit
from .exceptions import IsbnInvalidException


async def get_from_isbn(isbn: str) -> bool:
    if not isbn_check_digit(int(isbn)):
        logging.warning(msg=f"Invalid ISBN: {isbn}")
        raise IsbnInvalidException(f"ISBN {isbn} isn't valid.")
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay: {response.status_code}.')
        raise IsbnInvalidException(f"Failed to get book from API, response {response.status_code}.")
    result = json.loads(response.text)
    if result['totalItems'] <= 0:
        logging.warning(f'No volumes found for {isbn}.')
        raise IsbnInvalidException(f"No books found for ISBN {isbn}.")
    item = result['items'][0]
    logging.info(msg=f"Book name {item['volumeInfo']['title']} found.")
    date_of_publishing_string = item['volumeInfo']['publishedDate']
    try:
        publishing_date = datetime.strptime(date_of_publishing_string, "%Y-%m-%d")
    except ValueError as e:
        try:
            publishing_date = datetime.strptime(date_of_publishing_string, "%Y")
        except ValueError as e:
            logging.warning(f"Couldn't save book date {date_of_publishing_string}, so just using now.")
            publishing_date = datetime.now()
    return Book(title=item['volumeInfo']['title'], author=item['volumeInfo']['authors'][0], isbn=isbn,
                date_of_publishing=publishing_date), True
