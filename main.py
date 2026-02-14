from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_resume_text
from keyword_extractor import extract_keywords
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

    # Decide how to get JD text
    if job_description:
        jd_text = job_description

    elif jd_file:
        jd_text = await extract_text_from_file(jd_file)

    else:
        return {"error": "Please provide either job_description text or upload jd_file"}

    jd_keywords = extract_keywords(jd_text)

    return {
        "resume_preview": resume_text[:300],
        "jd_keywords": jd_keywords
    }
