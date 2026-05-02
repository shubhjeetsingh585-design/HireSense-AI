import subprocess
import json
import re

def extract_keywords_ai(text):
    prompt = f"""
You are an ATS keyword analyzer.

Extract ONLY meaningful technical keywords from this job description.

STRICT RULES:
- Output ONLY JSON (no explanation, no markdown)
- Do NOT include generic words like: experience, knowledge, strong
- Focus ONLY on:
  - programming languages
  - frameworks
  - tools
  - technologies
  - technical concepts

Format:
{{
  "keywords": ["python", "react", "aws"]
}}

Job Description:
{text}
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
        print("\n--- RAW KEYWORD LLM OUTPUT ---\n", output, "\n")
        match = re.search(r"\{[\s\S]*\}", output)
        if match:
            try:
                data = json.loads(match.group(0))
                keywords = data.get("keywords", [])
                cleaned = [
                    k.lower().strip()
                    for k in keywords
                    if isinstance(k, str) and len(k.strip()) > 2
                ]
                return list(set(cleaned))
            except Exception as e:
                print("Keyword JSON parsing failed:", e)
        words = re.findall(r"\b[a-zA-Z\+\#\.]{3,}\b", output.lower())
        blacklist = {
            "and", "the", "with", "for", "this", "that",
            "keywords", "output", "json", "only",
            "extract", "meaningful"
        }
        filtered = [
            w for w in words
            if w not in blacklist and len(w) > 2
        ]
        return list(set(filtered[:10]))
    except Exception as e:
        print("Keyword Extract Error:", e)
        return []