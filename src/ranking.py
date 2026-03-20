import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resume(clean_resume, clean_jd, top_n=5):
    if not clean_resume or not clean_jd:
        return [], np.array([])

    tfidf = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1,2)
    )

    resume_vectors = tfidf.fit_transform(clean_resume)

    jd_vector = tfidf.transform([clean_jd])

    similarity_score = cosine_similarity(jd_vector, resume_vectors).flatten()

    top_indices = np.argsort(similarity_score)[::-1][:top_n]

    return top_indices.tolist(), similarity_score