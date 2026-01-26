from preprocessing import transform_text
from ranking import rank_resume
from skills import extract_skills

def run_resume_screening(
    resumes,
    job_description,
    skill_vocab,
    top_n=5
):
    # 1. preprocessing
    clean_resume = [transform_text(r) for r in resumes]

    # 2. preprocessing job discription
    clean_jd = transform_text(job_description)

    # 3. rank resumes
    top_indices, scores = rank_resume(clean_resume, clean_jd, top_n)

    # 4. Exract JD skills
    # jd_skills = extract_skills(clean_jd, skill_vocab)
    skill_vocab = set(skill_vocab)
    results = []
    # 5. Skill-gap analysis
    for rank, idx in enumerate(top_indices, start=1):

        resume_text = clean_resume[idx]
        resume_skills = extract_skills(resume_text, skill_vocab)
        resume_skills = set(resume_skills)

        matched_skills = sorted(skill_vocab & resume_skills)
        missing_skills = sorted(skill_vocab - resume_skills)
    

        results.append({
            "rank": rank,
            "score": round((len(matched_skills) / len(skill_vocab)) * 100, 2),
            "missing_skills":list(missing_skills),
            "matched_skills": matched_skills,
            "resume_index":idx
        })
    return results

