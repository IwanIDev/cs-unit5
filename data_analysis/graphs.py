import database as db
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


def top_genres_chart(database: db.Database) -> Image:
    sql = """
    SELECT Genre, COUNT(Genre) AS totalvalue FROM Books
    GROUP BY Genre
    ORDER BY totalvalue DESC
    """  # Copied this query from recommendations.suggestions

    res = pd.read_sql(sql, database.connection)
    df = pd.DataFrame(data=res, columns=['Genre', 'totalvalue'])
    df = df[df.Genre != ""]  # Filters out blank genres.
    graph = plt.pie(df['totalvalue'], labels=df['Genre'], autopct='%.2f')
    img_buf = BytesIO()
    img_buf.seek(0)
    plt.savefig(img_buf, format='png')

    image = Image.open(img_buf)
    return image
