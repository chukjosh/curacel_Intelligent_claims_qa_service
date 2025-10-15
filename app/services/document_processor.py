"""Document text extraction service for PDFs and images."""
from io import BytesIO
from typing import Literal
import PyPDF2
from PIL import Image
import pytesseract

class DocumentProcessor:
    @staticmethod
    def extract_text(file_content: bytes, file_type: Literal["pdf", "image"]) -> str:
        """
        Extract text from PDF or image file.

        Args:
            file_content: Raw bytes of the file.
            file_type: 'pdf' or 'image'.

        Returns:
            Extracted text as a string.
        """
        if file_type.lower() == "pdf":
            return DocumentProcessor._extract_pdf_text(file_content)
        elif file_type.lower() == "image":
            return DocumentProcessor._extract_image_text(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _extract_pdf_text(file_content: bytes) -> str:
        """Extract text from PDF using PyPDF2."""
        try:
            pdf_file = BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract PDF text: {str(e)}") from e

    @staticmethod
    def _extract_image_text(file_content: bytes) -> str:
        """Extract text from an image using Pillow + Tesseract OCR."""
        try:
            image = Image.open(BytesIO(file_content))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract image text: {str(e)}") from e
