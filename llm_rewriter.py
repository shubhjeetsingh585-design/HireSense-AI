import subprocess
import re

def rewrite_resume_sections(resume_text, jd_text, missing_skills):
    prompt = f"""
You are an expert ATS resume optimizer.

Rewrite ONLY:
1. Career Objective
2. Skills Section
3. Projects Section

STRICT RULES:
- Do NOT add fake experience or specific tools not present in resume
- You MAY include missing skills ONLY as:
  - "familiar with", "exposure to", or "basic knowledge of"
- Do NOT claim production experience for missing skills
- Keep it realistic for a student profile
- Keep professional tone
- Do NOT include job description
- Do NOT add new sections

Missing Skills to consider:
{missing_skills}

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
        print("\n--- RAW LLM REWRITE OUTPUT ---\n", output, "\n")

        #Remove escape characters
        
        cleaned = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)

        #Normalize spacing
        
        cleaned = re.sub(r'\n+', '\n', cleaned)

        #Fallback safety
        
        if not cleaned or len(cleaned) < 20:
            return "Resume rewrite could not be generated properly."
        return cleaned.strip()
    except Exception as e:
        print("LLM Error:", e)
        return "LLM processing failed"