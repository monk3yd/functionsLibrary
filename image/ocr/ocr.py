
def show_image(title: str, image):
    cv2.imshow(title, image)  # open image
    cv2.moveWindow(title, 450, 50)  # center window
    cv2.waitKey(5000)  # delay
    cv2.destroyAllWindows()  # close


def resize_image(image, scale_percent: int):
    # Resize image
    # https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    print(f"Original Dimensions : {image.shape}")
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    print(f"Resized Dimensions : {image.shape}")
    return image