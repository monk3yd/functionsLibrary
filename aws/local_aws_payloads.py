import random

from pathlib import Path
from utils import transform_image_to_b64str

# --- LOCAL TESTING INPUT LOADS ---

# test_api_key = "6KH@2T4g2geP"
images = [
    "../tests/images/image1.jpeg",
    # "../tests/images/image2.jpeg",
    # "../tests/images/image3.png",
    # "../tests/images/image4.png",
    # "../tests/images/image5.jpeg",
    # "../tests/images/image6.jpeg",
    # "../tests/images/image7.jpeg",
    # "../tests/images/image8.png",
    # "../tests/images/image9.png",
]

img = random.choice(images)
b64image = transform_image_to_b64str(Path(img))

# Wrong test loads
# test_api_key = "2KH@aT4u2geP"
# Broken image testload (no QR detected)
# img_path = Path("localtest/test_image4.png")
# img_path = Path("localtest/test_image5.jpeg")

# Broken image testload (incorrect file extension or inner format)
# img_path = Path("localtest/giphy.gif")

# No image workload
# img_path = Path("")

