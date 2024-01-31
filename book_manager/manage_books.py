import httpx
from book_manager import Book
from typing import Optional
import json
import logging
from datetime import datetime


def get_from_isbn(isbn: str) -> Optional[Book]:
    r = httpx.get(url=f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if r.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay: {r.status_code}.')
        return None
    result = json.loads(r.text)
    if result['totalItems'] <= 0:
        logging.warning(f'No volumes found for {isbn}.')
        return None
    item = result['items'][0]
    return Book(title=item['volumeInfo']['title'], author=item['volumeInfo']['authors'][0], isbn=isbn,
                date_of_publishing=datetime.strptime(item['volumeInfo']['publishedDate'], "%Y-%m-%d"))
