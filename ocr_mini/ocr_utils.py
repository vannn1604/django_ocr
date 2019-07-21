try:
    from PIL import Image as Image_ocr
except ImportError:
    import Image as Image_ocr
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def ocr(filename):
    return pytesseract.image_to_string(Image_ocr.open(filename))
