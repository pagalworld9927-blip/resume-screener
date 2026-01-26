import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


PROTECTED_WORDS = {
    'it', 'ms', 'sql', 'aws', 'ai', 'ml', 'ui', 'ux',
    'c', 'c++', 'c#'
}

def transform_text(text):
    text = re.sub('[^a-zA-Z0-9]+#', ' ',text)

    text = text.lower()
    
    words = text.split()

    cleaned_words = []
    for word in words:
        if word in PROTECTED_WORDS:
            cleaned_words.append(word)
            continue
        
        if word in stop_words:
            continue
        if len(word) <= 2 and word not in ['ai', 'ml', 'ms']:
            continue
        cleaned_words.append(lemmatizer.lemmatize(word))
    
    return ' '.join(cleaned_words)


