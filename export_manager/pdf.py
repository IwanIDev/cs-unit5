from data_analysis import top_genres_chart
from pathlib import Path
import database as db
from io import BytesIO
from datetime import datetime
from PIL import Image
import logging
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import reportlab.platypus as platypus


def generate_pdf(path: Path, database: db.Database) -> None:
    buffer = BytesIO()
    w, h = A4
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(50, h - 50, "Library Report")
    current_datetime = datetime.now()
    c.drawString(50, h - 70, current_datetime.strftime("%A, %d/%m/%Y at %H:%M"))

    top_genres: Image = top_genres_chart(database)
    iw, ih = top_genres.size
    aspect = ih / float(iw)
    desired_width = int(w * 0.7)
    top_genres = top_genres.resize((desired_width, int(desired_width * aspect)), Image.Resampling.LANCZOS)
    logging.warning(f"Size is {top_genres.size[0]}x{top_genres.size[1]}.  Was {iw}x{ih}.")
    reportlab_chart = ImageReader(top_genres)
    c.drawImage(image=reportlab_chart, x=50, y=(h / 2))

    with open(str(path), "wb") as f:
        c.save()
        buffer.seek(0)
        f.write(buffer.getvalue())
