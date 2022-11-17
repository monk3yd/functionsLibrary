import random

from pathlib import Path
from pdf_utils import transform_pdf_to_b64str

# --- LOCAL TESTING INPUT LOADS ---

# test_api_key = "6KH@2T4g2geP"
files = [
    # "../tests/pdfs/color.pdf",
    "../tests/pdfs/blackandwhite.pdf",
]

file = random.choice(files)

b64pdf = transform_pdf_to_b64str(Path(file))

# b64image = transform_image_to_b64str(Path(file))
