import io
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from fastapi import UploadFile, HTTPException
from app.core.logging import get_logger

logger = get_logger(__name__)

async def parse_document(file: UploadFile) -> str:
    """
    Parse an uploaded document (PDF or Image) and extract text.
    Uses PyMuPDF for PDFs. If text is near-empty, falls back to OCR via pdf2image + pytesseract.
    For images, uses pytesseract directly.
    """
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith(".pdf"):
        return _parse_pdf(content)
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return _parse_image(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, PNG, or JPEG.")

def _parse_pdf(content: bytes) -> str:
    # 1. Try PyMuPDF text extraction
    final_text = ""
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            
            # 2. Check if page has alphanumeric text
            has_alnum = any(c.isalnum() for c in page_text)
            
            if has_alnum:
                final_text += page_text + "\n"
            else:
                # 3. Fallback to OCR for this specific page
                logger.info(f"Page {page_num} lacks alphanumeric text. Falling back to OCR.")
                final_text += _ocr_pdf_page(content, page_num) + "\n"
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")

    return final_text

def _ocr_pdf_page(content: bytes, page_num: int) -> str:
    try:
        # Convert specific PDF page to image
        # Note: poppler must be installed on the system for this to work
        images = convert_from_bytes(content, first_page=page_num+1, last_page=page_num+1)
        if images:
            return pytesseract.image_to_string(images[0])
    except Exception as e:
        logger.error(f"OCR failed for page {page_num}. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR failed. Is tesseract/poppler installed? Error: {str(e)}")
        
    return ""

def _parse_image(content: bytes) -> str:
    try:
        img = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image OCR failed: {str(e)}")
