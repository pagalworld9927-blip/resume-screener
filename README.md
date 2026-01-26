# Resume Screening System (Multi-Department)

An end-to-end resume screening web application that ranks resumes against a job description,
identifies matched and missing skills, and provides explainable scoring.
The system supports multiple departments and roles and allows resume upload in PDF format.

---

## 🚀 Features

- Multi-department & role-based screening  
- Automatic job description & skill loading per role  
- Resume ranking using text similarity  
- Skill-gap analysis (matched vs missing skills)  
- PDF resume upload support  
- Explainable score with clear measurement scale  
- Web UI built with Streamlit  

---

## 🧠 How the System Works

1. **Role Selection**
   - User selects a department and role
   - System loads predefined required skills and a default job description

2. **Resume Input**
   - Upload a PDF resume **or**
   - Use resumes from a dataset

3. **Preprocessing**
   - Resume text and job description are cleaned and normalized
   - No data leakage between resume and job description

4. **Ranking**
   - Resumes are ranked using text similarity with the job description

5. **Skill Analysis**
   - Required skills are compared with resume skills
   - Matched skills and missing skills are calculated using set logic

6. **Scoring**
   - Score = (Matched Skills / Required Skills) × 100
   - Results are shown with interpretation and visual indicators

---

## 📊 Score Interpretation

| Score Range | Meaning |
|------------|--------|
| 80–100% | Excellent Match |
| 60–79% | Good Match |
| 40–59% | Weak Match |
| Below 40% | Poor Match |

> This score is a screening aid, not a hiring decision.

---

## 🏢 Supported Departments

- Accountant  
- Advocate  
- Agriculture  
- Apparel  
- Arts  
- Automobile  
- Banking  
- BPO  
- Business Development  
- Chef  
- Construction  
- Designer  
- Digital Media  
- Engineering  
- Finance  
- Fitness  
- Healthcare  
- HR  
- Information Technology  
- Public Relation  
- Sales  
- Teacher  

Each department has role-specific skills and job descriptions defined in `roles_config.py`.

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Pandas  
- Scikit-learn  
- PyPDF / PyPDF2  

---

## 📁 Project Structure

