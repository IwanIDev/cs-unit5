import httpx
from book_manager import Book
from typing import Tuple, Optional
import json
import logging
from datetime import datetime
from utils import isbn_check_digit


async def get_from_isbn(isbn: str) -> Tuple[Optional[Book], bool]:
    if not isbn_check_digit(int(isbn)):
        logging.warning(msg=f"Invalid ISBN: {isbn}")
        return None, False
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay: {response.status_code}.')
        return None, False
    result = json.loads(response.text)
    if result['totalItems'] <= 0:
        logging.warning(f'No volumes found for {isbn}.')
        return None, False
    item = result['items'][0]
    logging.info(msg=f"Book name {item['volumeInfo']['title']} found.")
    return Book(title=item['volumeInfo']['title'], author=item['volumeInfo']['authors'][0], isbn=isbn,
                date_of_publishing=datetime.strptime(item['volumeInfo']['publishedDate'], "%Y-%m-%d")), True
