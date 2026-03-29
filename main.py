from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_resume_text
from keyword_extractor import extract_keywords
from skill_extractor import extract_skills
from matcher import match_skills
from ats_score import calculate_ats_score
from llm_rewriter import rewrite_resume

import PyPDF2
import docx
import io

app = FastAPI()


async def extract_text_from_file(file: UploadFile):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    elif file.filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])

    elif file.filename.endswith(".txt"):
        return content.decode("utf-8")

    else:
        return None


@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(None),
    jd_file: UploadFile = File(None)
):

    # Extract resume text
    resume_text = await extract_resume_text(resume)

    # Decide JD input
    if job_description:
        jd_text = job_description

    elif jd_file:
        jd_text = await extract_text_from_file(jd_file)

    else:
        return {"error": "Please provide either job_description text or upload jd_file"}


    jd_keywords = extract_keywords(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills, missing_skills = match_skills(resume_skills, jd_skills)

    ats_score = calculate_ats_score(matched_skills, len(jd_skills))

    rewritten_resume = rewrite_resume(
        resume_text[:500],
        jd_text[:300]
    )
    suggestions = [
    f"Add or improve experience in {skill}"
    for skill in missing_skills
    ]

    return {
        "resume_preview": resume_text[:300],
        "jd_keywords": jd_keywords,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "rewritten_resume": rewritten_resume,
        "suggestions": suggestions
    }