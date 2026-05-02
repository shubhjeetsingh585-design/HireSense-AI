import pdfplumber
import docx
import io

async def extract_resume_text(file):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print("Resume PDF extraction error:", e)
            return ""
        return clean_text(text)
    elif file.filename.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return clean_text(text)
        except Exception as e:
            print("Resume DOCX extraction error:", e)
            return ""
    return ""
def clean_text(text):
    if not text:
        return ""

    # Remove extra spaces & newlines
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()