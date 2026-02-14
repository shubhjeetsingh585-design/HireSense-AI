from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_resume_text
from keyword_extractor import extract_keywords
app = FastAPI()
@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = await extract_resume_text(resume)
    jd_keywords = extract_keywords(job_description)
    return {
        "resume_text_preview": resume_text[:300],
        "jd_keywords": jd_keywords
    }