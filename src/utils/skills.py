import re
def extract_skills(text, skill_vocab):

    if not text:
        return set()
    text = " " +  text.lower() + " "
    found_skills = set()
    for skill in skill_vocab:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills



