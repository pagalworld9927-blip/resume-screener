import streamlit as st 
import pandas as pd
import logging
import os
import sys
from src.exceptions import CustomException
from src.pipeline.pipeline import run_resume_screening
from src.components.preprocessing import transform_text
from src.components.pdf_reader import extract_text_from_pdf
from src.config.roles_config import ROLES

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Resume Screener", layout="wide")

st.title(" Resume Screening system")
st.write("Paste a Job Description and rank resumes with skill-gap analysis.")

# load dataset
@st.cache_data
def load_resumes():
    try:
        logger.info("load_resume function called.")
        base_dir = os.path.dirname(__file__)
        data_path = os.path.join(base_dir, "dataset", "Resume", "Resume.csv")
        df = pd.read_csv(data_path)
        logger.info("Resume load succesfully.")
        return df['Resume_str'].dropna().tolist()
    except Exception as e:
        logger.error("Load resume Failed: %s", str(e))
        raise CustomException(e, sys)


# score measure scale
def score_scale(score: float):
    logger.info("score_scale function called")
    if score >= 80:
        return {
            "label": "Excellent Match",
            "range": "80–100%",
            "desc": "Strong alignment with the job description. Resume is highly relevant.",
            "emoji": "🟢"
        }
    elif score >= 60:
        return {
            "label": "Good Match",
            "range": "60–79%",
            "desc": "Meets most requirements but has some skill gaps.",
            "emoji": "🟡"
        }
    elif score >= 40:
        return {
            "label": "Weak Match",
            "range": "40–59%",
            "desc": "Partial match. Significant upskilling required.",
            "emoji": "🟠"
        }
    else:
        return {
            "label": "Poor Match",
            "range": "0–39%",
            "desc": "Does not meet core job requirements.",
            "emoji": "🔴"
        }


# ui input
left_col, right_col = st.columns([1,2])

with left_col:
    st.subheader("Role Selection")

    department = st.selectbox(
        "Select Deparment",
        list(ROLES.keys())
    )

    role = st.selectbox(
        "Select Role",
        list(ROLES[department].keys())
    )

    role_data = ROLES[department][role]

    job_description = st.text_area(
        "Job Description",
        value=role_data["job_description"],
        height=220
    )
    SKILLS=role_data["skills"]


    mode = st.radio(
        "choose resume source",
        ["Use dataset resumes", "upload PDF resume"]
    )

    uploaded_pdf = None
    if mode == "upload PDF resume":
        uploaded_pdf = st.file_uploader(
            "Upload Resume (pdf)",
            type=["pdf"]
        )

    top_n = st.slider("Number of top resumes", 1, 10, 3)

    analyze_btn = st.button("Analyze Resumes")

# run pipeline
with right_col:
    st.subheader(" Results")
    results = []
    if analyze_btn:
        if not job_description.strip():
            logger.warning("job description is empty")
            st.warning("Please paste a job description")
        else:
            with st.spinner("Anlyzing Resumes..."):
                logger.info("Analyze button clicked. Mode: %s", mode)

                if mode == "Use dataset resumes":
                    resumes = load_resumes()
                    logger.info("Data sets resume loaded. Count: %d", len(resumes))
                    effective_top_n = top_n
                else:
                    if uploaded_pdf is None:
                        st.warning("Please upload a PDF resume.")
                        st.stop()
                    pdf_text = extract_text_from_pdf(uploaded_pdf)
                    logger.info("Pdf text extracted. Character %d", len(pdf_text))
                    resumes = [pdf_text]
                    effective_top_n = 1
                
                results =  run_resume_screening(
                resumes=resumes,
                job_description= job_description,
                skill_vocab=SKILLS,
                top_n=effective_top_n
            )
            logger.info("pipeline completed.")

    st.success("Analysis Complete!")

# Display Result

    for r in results:
        meta = score_scale(r["score"])
        with st.expander(
             f"{meta['emoji']} Rank #{r['rank']} | Score: {r['score']} – {meta['label']}"
        ):
            st.progress(r["score"] / 100)
            st.markdown(f"**Score Range:** {meta["range"]}")
            st.markdown(f"**Verdict:** {meta['desc']}")

            st.divider()

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Matched Skills")
                if r["matched_skills"]:
                    st.write(", ".join(r["matched_skills"]))
                else:
                    st.write("No core skills matched.")

            with col2:
                st.markdown("### ❌ Missing Skills")
                if r["missing_skills"]:
                    st.write(", ".join(r["missing_skills"]))
                else:
                    st.write("No major skill gaps.")

            
