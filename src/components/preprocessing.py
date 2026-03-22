import re
import logging
import nltk
from nltk.corpus import stopwords
from src.exceptions import CustomException
import sys

import src.loggers  # activates the logging config (creates log file, sets format & level)

# Create a logger for this specific module
logger = logging.getLogger(__name__)


try:
    logger.info("Loading NLTK stopwords...")
    stop_words = set(stopwords.words("english"))
    logger.info("Stopwords loaded successfully. Total words: %d", len(stop_words))
except LookupError:
    logger.warning("Stopwords not found locally. Downloading from NLTK...")
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    logger.info("Stopwords downloaded and loaded. Total words: %d", len(stop_words))


def transform_text(text):
    if not text:
        logger.warning("transform_text() received empty or None input.")
        return ""
    try:
        logger.info("Starting text transformation. Input length: %d", len(text))

        text = text.lower()
        text = re.sub('[^a-zA-Z0-9]+#', ' ', text)
        text = re.sub(r"\s+", " ", text)
        result = text.strip()

        logger.info("Text transformation complete. Output length: %d", len(result))
        return result
    except Exception as e:
        logger.error("Text transformation Failed: %s", str(e))
        raise CustomException(e, sys)


    


