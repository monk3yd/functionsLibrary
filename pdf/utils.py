# Useful transform PDF functions

import base64
import pdfplumber

from pathlib import Path
from pdf2image import convert_from_path


def transform_pdf_to_b64str(pdf: Path) -> str:
    """
    Input: PDF file path
    Output: base64 encoded PDF string
    """
    with open(pdf, "rb") as pdf_file:
        byte_encoded_string = base64.b64encode(pdf_file.read())
        pdf_string = byte_encoded_string.decode()
        return pdf_string


def transform_b64str_to_pdf(pdf_string: str, pdf_path=Path("/tmp/input.pdf")) -> Path:
    """
    Input: PDF base64 encoded string
    Output: Path to saved PDF file
    """
    byte_decoded_string = base64.b64decode(pdf_string)
    with open(pdf_path, "wb") as pdf:
        pdf.write(byte_decoded_string)
    return pdf_path


def transform_pdf_to_images(path: Path) -> list:
    """
    Input: PDF's Path
    Output: list of JPEG images (1 pdf page per image)
    """
    # Store all pages of pdf in variable
    image_file_list = []

    # Read pdf file at 500 DPI
    pdf_pages = convert_from_path(path, 500)

    # Iterate through pages
    for page_enumeration, page in enumerate(pdf_pages, start=1):
        filename = f"/tmp/page_{page_enumeration:03}.jpg"

        # Save the image of pdf page in system
        page.save(filename, "JPEG")
        image_file_list.append(filename)

    return image_file_list


def extract_pdf_text(path: Path) -> str:
    """
    Input: PDF Path
    Output: Text embedded in 'original' PDF
    """
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        pdf_text = first_page.extract_text()
    return pdf_text
