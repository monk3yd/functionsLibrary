import cv2
import json

from kraken import binarization
from PIL import Image
from pyzbar import pyzbar
from utils import transform_b64str_to_image


class QRHandler:
    def __init__(self):
        self.scan_success = True
    
    def scan(self, image: str or bytes):
        cv_image = transform_b64str_to_image(image)  # numpy darray

        # resize image
        scale = 1.3
        width = int(cv_image.shape[1] * scale)
        height = int(cv_image.shape[0] * scale)
        image = cv2.resize(cv_image, (width, height))
        image = Image.fromarray(image)

        # binarization
        bw_image = binarization.nlbin(image)
        # bw_img.save("/tmp/resized_and_binarized.png")

        # Decode embedded QR
        qr_data_obj = pyzbar.decode(
            bw_image,
            symbols=[pyzbar.ZBarSymbol.QRCODE]
        )

        try:
            qr_data = json.loads(qr_data_obj[0].data.decode("utf-8"))
        except IndexError:
            self.scan_success = False
            return {
                "success": self.scan_success,
                "message": "Wasn't able to read QR code."
            }
        else:
            if "rut" not in qr_data:
                self.scan_success = False
                return {
                    "success": self.scan_success,
                    "message": "No data was found from QR scan."
                }

        # 200OK
        return {
            "success": self.scan_success,
            "body": qr_data
        }