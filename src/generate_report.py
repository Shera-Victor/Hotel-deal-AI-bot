from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from datetime import datetime

def generate_pdf(deals):
    os.makedirs("reports", exist_ok=True)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    html = template.render(
        date=datetime.now().strftime("%d %b %Y"),
        deals=deals
    )

    output_path = f"reports/hotel_report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdfkit.from_string(html, output_path)
    return output_path
