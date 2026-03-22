import logging
import sys
import src.loggers
from pypdf import PdfReader
from src.exceptions import CustomException

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file):
    logger.info("Starting PDF extraction for: %s", pdf_file)

    try:
        reader = PdfReader(pdf_file)
        logger.info("PDF opened. Pages found %d", len(reader.pages))
        text = ""
        # for page in reader.pages:
        #     text += page.extract_text() or ""
        # logger.info("Extraction done. Characters: %d", len(text))

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            
            if not page_text:
                logger.warning("Page %d has no text", page_num + 1)
            text += page_text
        logger.info("Extraction done. Characters: %d", len(text))
        return text
    except Exception as e:
        logger.error("something went wrong: %s", str(e)) 
        raise CustomException(e, sys)