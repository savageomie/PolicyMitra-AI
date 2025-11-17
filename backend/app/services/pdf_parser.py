# Async PDF text extraction using PyMuPDF (fitz) with fallback
import asyncio

async def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from PDF bytes using PyMuPDF (fitz). Fallback to bytes.decode if needed.
    """
    try:
        import fitz  # PyMuPDF
        def _extract():
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = "".join([page.get_text() for page in doc])
            doc.close()
            return text
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _extract)
    except Exception:
        try:
            # Fallback: decode bytes
            return file_bytes.decode("latin-1", errors="ignore")
        except Exception:
            return ""