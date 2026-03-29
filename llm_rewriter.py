import subprocess

def rewrite_resume(resume_text, jd_text):
    prompt = f"""
You are an expert ATS resume optimizer.

Rewrite the resume to better match the job description.

STRICT RULES:
- Do NOT add explanations or notes
- Do NOT mention modifications
- Do NOT include job description
- Keep only resume content
- Improve wording and keywords

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout