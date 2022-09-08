import base64
import pdfplumber

from pathlib import Path
from pdf2image import convert_from_path


def pdf_to_str(pdf: Path) -> str:
    """
    Input PDF's Path -> Returns encoded PDF string
    """
    with open(pdf, "rb") as pdf_file:
        byte_encoded_string = base64.b64encode(pdf_file.read())
        pdf_string = byte_encoded_string.decode()
        return pdf_string


def pdf_str_to_file(pdf_string: str, pdf_path=Path("/tmp/input.pdf")) -> Path:
    """
    Reconstruct PDF's string & save it into file. Returns Path
    """
    byte_decoded_string = base64.b64decode(pdf_string)
    with open(pdf_path, "wb") as pdf:
        pdf.write(byte_decoded_string)
    return pdf_path


def pdf_to_image(path: Path) -> list:
    """
    Input PDF's Path -> Returns jpeg image
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
    Extracts text from original PDF
    """
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        pdf_text = first_page.extract_text()
    return pdf_text
