import numpy as np
import logging
import src.loggers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
from src.exceptions import CustomException

logger = logging.getLogger(__name__)

def rank_resume(clean_resume, clean_jd, top_n=5):
    if not clean_resume or not clean_jd:
        return [], np.array([])
    try:
        tfidf = TfidfVectorizer(
            max_features=3000,
            ngram_range=(1,2)
        )

        resume_vectors = tfidf.fit_transform(clean_resume)
        logger.info("resume vectors are created %s", resume_vectors.shape)

        jd_vector = tfidf.transform([clean_jd])
        logger.info("Job description vectors are created %s", jd_vector.shape)

        similarity_score = cosine_similarity(jd_vector, resume_vectors).flatten()
        logger.info("similarity score between job description adn resume %s", similarity_score)

        top_indices = np.argsort(similarity_score)[::-1][:top_n]
        logger.info("Top %d indices selected %s",top_n, top_indices)

        return top_indices.tolist(), similarity_score
    except Exception as e:
        logger.error("Ranking Failed: %s", str(e))
        raise CustomException(e, sys)