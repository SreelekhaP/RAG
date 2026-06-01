import os
from pathlib import Path
from typing import List, Tuple
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

class TextExtractor:
    def __init__(self):
        # Look for Windows Tesseract installation path dynamically
        tesseract_cmd = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        if os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts text layer directly, using progressive OCR fallbacks for scanned sheets."""
        doc = fitz.open(pdf_path)
        pages_text = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text().strip()

            # Fallback 1: PyMuPDF integrated OCR engine
            if not text:
                text = self._ocr_page_with_pymupdf(page)

            # Fallback 2: Classic Tesseract OCR via image conversion
            if not text.strip():
                text = self._ocr_page_with_tesseract(page)

            pages_text.append(f"\n--- Page {page_num + 1} ---\n{text}")

        doc.close()
        return "\n".join(pages_text)

    def _ocr_page_with_pymupdf(self, page) -> str:
        try:
            tp = page.get_textpage_ocr(flags=fitz.TEXT_PRESERVE_WHITESPACE)
            return page.get_text(textpage=tp).strip()
        except Exception:
            return ""

    def _ocr_page_with_tesseract(self, page) -> str:
        try:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang="eng")
            return text.strip()
        except Exception as e:
            return f"[OCR Fallback Failure: {str(e)}]"

    def extract_text_from_directory(self, directory: str) -> List[Tuple[str, str]]:
        results = []
        folder = Path(directory)
        for pdf_file in folder.glob("*.pdf"):
            try:
                text = self.extract_text_from_pdf(str(pdf_file))
                results.append((pdf_file.name, text))
            except Exception as e:
                print(f"Skipping corrupt or unreadable file {pdf_file.name}: {e}")
        return results