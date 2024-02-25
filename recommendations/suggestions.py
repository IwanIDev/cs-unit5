import asyncio
import json
import pandas as pd
import httpx
import database as db
import logging
from book_manager import get_book_from_google_api_volume, Book
from typing import List


async def get_suggestions(row: pd.Series, database: db.Database) -> List[str]:
    genre_name = row['Genre']
    index = row['index']
    url = f'https://www.googleapis.com/books/v1/volumes?q=subject:"{genre_name}"'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != httpx.codes.OK:
        logging.error(f"Response {response.status_code} in {genre_name}.")
        pass
    result = json.loads(response.text)

    if result['totalItems'] <= 0:
        logging.error(f"No results found for {genre_name}.")
        pass

    books = []
    for i, item in enumerate(result['items'][:3]):  # Gets top three items
        book = get_book_from_google_api_volume(item, database)
        books.append(book)
        logging.warning(f"{index}, {i}, {book.title}")
    return books


async def get_suggested_books(database: db.Database) -> List[Book]:
    sql = """
    SELECT Genre, COUNT(Genre) AS totalvalue FROM Books
    GROUP BY Genre
    ORDER BY totalvalue DESC;
    """
    res = pd.read_sql(sql, database.connection)
    df = pd.DataFrame(data=res, columns=['Genre', 'totalvalue'])
    df = df[df.Genre != ""]
    top_ten_df = df.groupby('totalvalue').head(9).reset_index()
    sample = top_ten_df.sample(n=3, replace=True)

    books_list = await asyncio.gather(
        get_suggestions(sample.iloc[[0]].squeeze(), database),
        get_suggestions(sample.iloc[[1]].squeeze(), database),
        get_suggestions(sample.iloc[[2]].squeeze(), database)
    )  # I don't think this actually works.
    books = []
    for book in books_list:
        books.extend([x for x in book])
    logging.warning(books)
    return books
