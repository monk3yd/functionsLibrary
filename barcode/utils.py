import json

from pathlib import Path
from pyzbar import pyzbar

from pdf417decoder import PDF417Decoder
from PIL import Image


def scan_qr(base64img: str or bytes):
    cv_image = convert_2_image(base64img)  # numpy darray

    # resize image
    # resize_image()
    # scale = 1.3
    # width = int(cv_image.shape[1] * scale)
    # height = int(cv_image.shape[0] * scale)
    # image = cv.resize(cv_image, (width, height))
    # img = Image.fromarray(image)

    # binarization
    # bw_img = binarization.nlbin(img)
    # bw_img.save("/tmp/resized_and_binarized.png")

    # Decode embedded qr through libraries
    qr_data_obj = pyzbar.decode(
        # bw_img,
        cv_image,
        symbols=[pyzbar.ZBarSymbol.QRCODE]
    )

    qr_data = json.loads(qr_data_obj[0].data.decode("utf-8"))


def scan_pdf417(img_path: Path):
    '''Input image path, returns decoded embedded pdf417 code bar data'''
    image = Image.open(image_path)
    decoder = PDF417Decoder(image)
    if (decoder.decode() > 0):
        return decoder.barcode_data_index_to_string(0)
