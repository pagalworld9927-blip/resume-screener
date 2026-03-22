import logging
import src.loggers
import sys
from src.exceptions import CustomException
from src.components.preprocessing import transform_text
from src.components.ranking import rank_resume
from src.utils.skills import extract_skills

logger =logging.getLogger(__name__)

def run_resume_screening(
    resumes,
    job_description,
    skill_vocab,
    top_n=5
):
    try:
        # 1. preprocessing
        clean_resume = [transform_text(r) for r in resumes]
        logger.info("Transform the resume Done! %s", len(clean_resume))

        # 2. preprocessing job discription
        clean_jd = transform_text(job_description)
        logger.info("Transformation of job desciption Done! %s", clean_jd)

        # 3. rank resumes
        top_indices, scores = rank_resume(clean_resume, clean_jd, top_n)
        logger.info("Top %d indices are selected %s", top_n, top_indices)

        # 4. Exract JD skills
        # jd_skills = extract_skills(clean_jd, skill_vocab)
        skill_vocab = set(skill_vocab)
        logger.info("Unique skill are selected %s", skill_vocab)
        results = []
        # 5. Skill-gap analysis
        for rank, idx in enumerate(top_indices, start=1):

            resume_text = clean_resume[idx]
            resume_skills = extract_skills(resume_text, skill_vocab)
            resume_skills = set(resume_skills)

            matched_skills = sorted(skill_vocab & resume_skills)
            logger.info("Matched skills are selected %s", matched_skills)
            missing_skills = sorted(skill_vocab - resume_skills)
            logger.info("missing skill are extracted %s", missing_skills)
        

            results.append({
                "rank": rank,
                "score": round((len(matched_skills) / len(skill_vocab)) * 100, 2),
                "missing_skills":list(missing_skills),
                "matched_skills": matched_skills,
                "resume_index":idx
            })
        logger.info("Result are ready to show %s",results)
        return results
    except Exception as e:
        logger.error("Pipeline Failed: %s", str(e))
        raise CustomException(e, sys)

