import httpx
from book_manager import Book
import json
import logging
from datetime import datetime
from utils import get_platform_dir, isbn_checksum, length_check, get_temp_dir
from .exceptions import IsbnInvalidException
from .database import get_author_id
from typing import Dict
import database as db


def get_from_isbn(isbn: str, database: db.Database) -> Book:
    if not isbn_checksum(isbn):
        logging.warning(msg=f"Invalid ISBN: {isbn}")
        raise IsbnInvalidException(f"ISBN {isbn} isn't valid.")

    with httpx.Client() as client:
        response = client.get(url=f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    if response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay: {response.status_code}.')
        raise IsbnInvalidException(f"Failed to get book from API, response {response.status_code}.")

    result = json.loads(response.text)

    if result['totalItems'] <= 0:
        logging.warning(f'No volumes found for {isbn}.')
        raise IsbnInvalidException(f"No books found for ISBN {isbn}.")

    item = result['items'][0]
    book = get_book_from_google_api_volume(item, database)
    return book


def get_thumbnail(book: Dict, isbn: str) -> str:
    try:
        image_url = book['volumeInfo']['imageLinks']['thumbnail']
    except KeyError as e:
        logging.warning(f"No thumbnail found for {isbn}")
        return ""
    with httpx.Client() as client:
        image_response = client.get(url=image_url)
    if image_response.status_code != httpx.codes.OK:
        logging.warning(f'Status code not okay in cover image: {image_response.status_code}.')
        return ""
    return image_response


def create_thumbnail_from_book(isbn: str, database: db.Database) -> None:
    get_from_isbn(isbn, database)
    return


def get_book_from_google_api_volume(item: Dict, database: db.Database) -> Book:
    # TODO JSON Validation
    logging.info(msg=f"Book name {item['volumeInfo']['title']} found.")
    isbn = 0
    try:
        isbn_list = item['volumeInfo']['industryIdentifiers']
        for isbn_dict in isbn_list:
            if isbn_dict['type'] != "ISBN_10":
                continue
            isbn = isbn_dict['identifier']
            break
    except KeyError:
        pass
    try:
        date_of_publishing_string = item['volumeInfo']['publishedDate']
    except KeyError:
        date_of_publishing_string = ""
    try:
        genre_name = item['volumeInfo']['categories'][0]
    except KeyError:
        genre_name = ""
    author_name = item['volumeInfo']['authors'][0]
    author = get_author_id(author_name, database)

    image_response = get_thumbnail(item, isbn)
    image_path = get_temp_dir().resolve() / f"{isbn}.jpg"

    try:
        with open(image_path, 'wb') as f:  # This just saves the image to a file without asking any questions.
            if image_response:
                f.write(image_response.content)
    except PermissionError as e:
        logging.error(f"Permission error in getting image {image_path}, erroring out.")

    try:
        publishing_date = datetime.strptime(date_of_publishing_string, "%Y-%m-%d")
    except ValueError as e:
        try:
            publishing_date = datetime.strptime(date_of_publishing_string, "%Y")
        except ValueError as e:
            logging.warning(f"Couldn't save book date {date_of_publishing_string}, so just using now.")
            publishing_date = datetime.now()
    return Book(title=item['volumeInfo']['title'], author=author, isbn=isbn,
                date_of_publishing=publishing_date, genre=genre_name)

