import base64
from pathlib import Path


def main():
    b64str = transform_file_to_b64str(Path("test.pdf"))
    file_path = transform_b64str_to_file(b64str, Path("reconstructed.pdf"))
    print(file_path)


def transform_file_to_b64str(file_path: Path or str) -> str:
    """
    It supports PDF, JPEG and PNG file extensions.
    :input: path to file
    :output: file base64 encoded string
    """

    with open(file_path, "rb") as file:
        b64str = base64.b64encode(file.read())
        return b64str


def transform_b64str_to_file(b64str: str, file_path: Path) -> Path:
    """
    Supports PDF, JPEG and PNG file extensions. Beware though that the
    reconstructed file extension should be the same as the original file.

    :inputs: file base64 encoded string & path where to save file
    :output: path where reconstructed file was saved

    """

    decoded_str = base64.b64decode(b64str)
    with open(file_path, "wb") as file:
        file.write(decoded_str)
    return file_path


if __name__ == "__main__":
    main()
