import logging
import src.loggers
import re
import sys
from src.exceptions import CustomException

logger = logging.getLogger(__name__)

def extract_skills(text, skill_vocab):

    if not text:
        logger.warning("extract_skills() receive empty text. Returning empty set.")
        return set()

    try:
        text = " " +  text.lower() + " "
        logger.info("Text are in lower formate %s", len(text))
        found_skills = set()
        for skill in skill_vocab:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)
        logger.info("Skills are extracted %s", found_skills)
        return found_skills
    except Exception as e:
        logger.error("Extract skill Failed: %s", str(e))
        raise CustomException(e, sys)



