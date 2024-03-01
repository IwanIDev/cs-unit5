from data_analysis import top_genres_svg
from pathlib import Path
import database as db
from io import BytesIO
from datetime import datetime
import logging
from tempfile import NamedTemporaryFile
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import reportlab.platypus as platypus
from reportlab.graphics import renderPDF


def svg_to_drawing_scaled(w: int, svg: str):
    with NamedTemporaryFile(delete=False, mode='w+') as tf:
        tf.write(svg)
        tf.seek(0)
        svg_image = svg2rlg(tf.name)
    iw, ih = svg_image.width, svg_image.height
    aspect = ih / float(iw)
    desired_width = int(w)
    scale_x = desired_width / iw
    scale_y = (desired_width * aspect) / ih
    svg_image.scale(scale_x, scale_y)
    return svg_image


def generate_pdf(path: Path, database: db.Database) -> None:
    buffer = BytesIO()
    w, h = A4
    doc = platypus.SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    body_style = styles['Normal']
    heading_style = styles['Heading1']
    story = []

    story.append(platypus.Paragraph("Library App", heading_style))
    current_datetime = datetime.now()
    story.append(platypus.Paragraph(str(current_datetime.strftime("%A, %d/%m/%Y at %H:%M")), body_style))

    graphs = [
        top_genres_svg(database)
    ]

    for graph in graphs:
        drawing = svg_to_drawing_scaled(int(w*0.6), graph)
        story.append(drawing)
    doc.build(story)

    with open(str(path), 'wb') as f:
        buffer.seek(0)
        f.write(buffer.getvalue())


# def generate_pdf(path: Path, database: db.Database) -> None:
#     buffer = BytesIO()
#     w, h = A4
#     c = canvas.Canvas(buffer, pagesize=A4)
#     c.drawString(50, h - 50, "Library Report")
#     current_datetime = datetime.now()
#     c.drawString(50, h - 70, current_datetime.strftime("%A, %d/%m/%Y at %H:%M"))
#
#     top_genres: str = top_genres_svg(database)
#     svg_image = svg_to_drawing_scaled(int(w * 0.7), top_genres)
#     renderPDF.draw(svg_image, c, x=50, y=(h / 2))
#
#     with open(str(path), "wb") as f:
#         c.save()
#         buffer.seek(0)
#         f.write(buffer.getvalue())
