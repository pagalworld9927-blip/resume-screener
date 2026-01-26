import re
import nltk
from nltk.corpus import stopwords


try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


def transform_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub('[^a-zA-Z0-9]+#', ' ',text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

    


