# Useful Transform Image functions

import io
import base64
import cv2 as cv
import numpy as np

from PIL import Image
from pathlib import Path


def transform_image_to_b64str(img: Path) -> str:
    '''
    Input: image PATH
    Output: image base64 encoded string
    '''
    with open(img, "rb") as raw_image:
        base64img = base64.b64encode(raw_image.read())
    return base64img.decode("UTF-8")


def transform_b64str_to_image(base64_str: str):
    '''
    Input: image base64 encoded string
    Output: CV image
    '''
    imgdata = base64.b64decode(str(base64_str))
    image = Image.open(io.BytesIO(imgdata))
    return cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY)
    # return cv.cvtColor(np.array(image), cv.COLOR_BGR2RGB)
