import httpx
from book_manager import Book
from .database import get_author_id
import json
import logging
from datetime import datetime
from utils import get_platform_dir, isbn_checksum, length_check
from .exceptions import IsbnInvalidException
import database as db
import shutil


async def get_from_isbn(isbn: str, database: db.Database) -> Book:
    if not length_check(isbn, 10, 10):
        logging.warning(msg=f"Invalid ISBN: {isbn}")
        raise IsbnInvalidException(f"ISBN {isbn} isn't valid.")

    if not isbn_checksum(isbn):
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
        image_url = item['volumeInfo']['imageLinks']['thumbnail']
    except KeyError as e:
        logging.warning(f"No thumbnail found for {isbn}")
        #  Todo this still doesn't work though.
    image_path = get_platform_dir().resolve() / f"{isbn}.jpg"
    async with httpx.AsyncClient() as client:
        image_response = await client.get(url=image_url)
    if image_response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay in cover image: {image_response.status_code}.')

    with open(image_path, 'wb') as f:  # This just saves the image to a file without asking any questions.
        f.write(image_response.content)

    try:
        publishing_date = datetime.strptime(date_of_publishing_string, "%Y-%m-%d")
    except ValueError as e:
        try:
            publishing_date = datetime.strptime(date_of_publishing_string, "%Y")
        except ValueError as e:
            logging.warning(f"Couldn't save book date {date_of_publishing_string}, so just using now.")
            publishing_date = datetime.now()

    author_name = item['volumeInfo']['authors'][0]
    author = get_author_id(author_name, database)

    return Book(title=item['volumeInfo']['title'], author=item['volumeInfo']['authors'][0], isbn=isbn,
                date_of_publishing=publishing_date)
