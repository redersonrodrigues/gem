import io
import pytest
from PIL import Image
from app.utils import image_utils


def create_test_image(format="JPEG", size=(100, 100)):
    img = Image.new("RGB", size, color="red")
    buf = io.BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    buf.filename = f"test.{format.lower()}"
    return buf

def test_allowed_file():
    assert image_utils.allowed_file("foto.jpg")
    assert not image_utils.allowed_file("documento.pdf")

def test_validate_image_ok():
    img = create_test_image()
    image_utils.validate_image(img)

def test_validate_image_type_error():
    fake = io.BytesIO(b"notanimage")
    fake.filename = "fake.jpg"
    with pytest.raises(ValueError):
        image_utils.validate_image(fake)

def test_validate_image_size_error():
    big = create_test_image()
    big.filename = "big.jpg"
    big.seek(0, 2)
    big.write(b"0" * (3 * 1024 * 1024))  # 3MB
    big.seek(0)
    with pytest.raises(ValueError):
        image_utils.validate_image(big)
