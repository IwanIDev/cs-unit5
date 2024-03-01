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
