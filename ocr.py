import os
import pdfplumber
import pytesseract
from PIL import Image


def extract_text(path):
    text = ""
    path = str(path)
    if path.lower().endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    # fallback: rasterize page and run OCR
                    try:
                        img = page.to_image(resolution=150).original
                        text += pytesseract.image_to_string(img) + "\n"
                    except Exception:
                        continue
    else:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
    return text
