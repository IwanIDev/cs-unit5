import httpx
from book_manager import Book
from typing import Optional
import json
import logging
from datetime import datetime


async def get_from_isbn(isbn: str) -> Optional[Book]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay: {response.status_code}.')
        return None
    result = json.loads(response.text)
    if result['totalItems'] <= 0:
        logging.warning(f'No volumes found for {isbn}.')
        return None
    item = result['items'][0]
    return Book(title=item['volumeInfo']['title'], author=item['volumeInfo']['authors'][0], isbn=isbn,
                date_of_publishing=datetime.strptime(item['volumeInfo']['publishedDate'], "%Y-%m-%d"))
