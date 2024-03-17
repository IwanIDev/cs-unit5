import logging
from datetime import datetime
import database as db
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO, TextIOWrapper


def get_top_genres(database: db.Database) -> pd.DataFrame:
    sql = """
        SELECT Genre, COUNT(Genre) AS totalvalue FROM Books
        GROUP BY Genre
        ORDER BY totalvalue DESC
        """  # Copied this query from recommendations.suggestions

    res = pd.read_sql(sql, database.connection)
    df = pd.DataFrame(data=res, columns=['Genre', 'totalvalue'])
    df = df[df.Genre != ""]  # Filters out blank genres.
    return df


def get_all_books(database: db.Database) -> pd.DataFrame:
    sql = """
    SELECT Books.BookID, Books.Name, Books.DatePublished, Books.Genre, Books.AuthorID, Authors.Name
    FROM Books
    INNER JOIN Authors ON (Books.AuthorID == Authors.AuthorID);
    """

    res = pd.read_sql(sql, database.connection)
    df = pd.DataFrame(data=res)
    logging.warning(f"Columns {df.columns.values.tolist()}")
    df.DatePublished = df.DatePublished.apply(lambda x: datetime.fromtimestamp(x))
    df.reset_index(drop=True)
    return df


def all_books_chart(database: db.Database) -> Image:
    df = get_all_books(database)
    fig, axs = plt.subplots(1, 1)
    axs.axis('tight')
    axs.axis('off')
    cell_text = []
    for row in range(len(df)):
        cell_text.append(df.iloc[row])
    table = axs.table(cellText=cell_text, colLabels=df.columns, loc="center")
    img_buf = BytesIO()
    img_buf.seek(0)
    plt.savefig(img_buf, format='png')

    image = Image.open(img_buf)
    return image


def all_books_svg(database: db.Database) -> str:
    df = get_all_books(database)
    fig, axs = plt.subplots(1, 1)
    axs.axis('tight')
    axs.axis('off')
    cell_text = []
    for row in range(len(df)):
        cell_text.append(df.iloc[row])
    table = axs.table(cellText=cell_text, colLabels=df.columns, loc="center")
    img_buf = BytesIO()
    img_buf.seek(0)
    wrapper = TextIOWrapper(img_buf, encoding='utf-8')
    img = wrapper.read()
    return img


def top_genres_chart(database: db.Database) -> Image:
    df = get_top_genres(database)
    graph = plt.pie(df['totalvalue'], labels=df['Genre'], autopct='%.2f')
    img_buf = BytesIO()
    img_buf.seek(0)
    plt.savefig(img_buf, format='png')

    image = Image.open(img_buf)
    return image


def top_genres_svg(database: db.Database) -> str:
    df = get_top_genres(database)
    graph = plt.pie(df['totalvalue'], labels=df['Genre'], autopct='%.2f')
    img_buf = BytesIO()
    img_buf.seek(0)
    plt.savefig(img_buf, format='svg')
    img_buf.seek(0)
    wrapper = TextIOWrapper(img_buf, encoding='utf-8')
    img = wrapper.read()
    return img
