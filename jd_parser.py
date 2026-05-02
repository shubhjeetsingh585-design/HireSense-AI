import pdfplumber
import docx
import io

async def extract_jd_text(file):
    content = await file.read()

    #PDF Handling
    
    if file.filename.endswith(".pdf"):
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print("PDF extraction error:", e)
        return clean_text(text)

    #DOCX Handling
    
    elif file.filename.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs])
            return clean_text(text)
        except Exception as e:
            print("DOCX extraction error:", e)
            return ""

    #TXT Handling
    
    elif file.filename.endswith(".txt"):
        try:
            return clean_text(content.decode("utf-8"))
        except:
            return ""

    return ""

#TEXT CLEANING FUNCTION

def clean_text(text):
    if not text:
        return ""

    # Remove extra spaces

    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()