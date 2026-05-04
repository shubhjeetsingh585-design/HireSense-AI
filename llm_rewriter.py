import subprocess
import re
def rewrite_resume_sections(resume_text, jd_text, missing_skills):
    missing_skills = missing_skills[:5]
    prompt = f"""
You are an expert ATS resume optimizer.
Rewrite ONLY:
1. Career Objective
2. Skills Section
3. Projects Section
STRICT RULES:
- DO NOT add fake projects or fake experience
- DO NOT invent companies or achievements
- DO NOT include job description
- DO NOT add new sections
IMPORTANT:
- Include missing skills naturally:
{missing_skills}

- Only use phrases:
  "familiar with", "basic knowledge of", "exposure to"
- DO NOT mention Node.js or Express.js unless clearly present in resume
- Skills must appear clearly in Skills section
OUTPUT:
- Clean text
- No markdown
- No repetition
Resume:
{resume_text}
Job Description:
{jd_text}
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            encoding="utf-8",
            errors="ignore"
        )
        output = result.stdout.strip()
        cleaned = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)
        cleaned = re.sub(r'\*+', '', cleaned)
        cleaned = re.sub(r'\n{2,}', '\n', cleaned)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)
        cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)
        return cleaned.strip() if len(cleaned) > 50 else "Rewrite failed"
    except Exception as e:
        print("LLM Error:", e)
        return "LLM processing failed"