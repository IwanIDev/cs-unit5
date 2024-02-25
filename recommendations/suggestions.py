import json
import pandas as pd
import httpx
import database as db
import logging
from book_manager import get_book_from_google_api_volume, Book
from typing import List


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
    books = []

    for index, row in sample.iterrows():
        genre_name = row['Genre']
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

        logging.warning(result)

        for item in result['items'][:3]:  # Gets top three items
            book = get_book_from_google_api_volume(item, database)
            books.append(book)
    return books
