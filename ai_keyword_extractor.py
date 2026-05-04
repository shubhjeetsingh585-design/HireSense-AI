import subprocess
import json
import re
def extract_keywords_ai(text):
    prompt = f"""
Extract 15–20 technical keywords from this job description.
ONLY JSON OUTPUT:
{{ "keywords": [] }}
Focus on:
- languages
- frameworks
- tools
- concepts
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
        match = re.search(r"\{[\s\S]*\}", output)
        if match:
            data = json.loads(match.group(0))
            keywords = data.get("keywords", [])
            cleaned = []
            for k in keywords:
                if isinstance(k, str):
                    k = k.lower().strip()
                    # normalize
                    k = k.replace("node.js", "node")
                    k = k.replace("express.js", "express")
                    k = k.replace("react.js", "react")
                    k = k.replace("restapi", "rest api")
                    if len(k) > 2:
                        cleaned.append(k)
            # remove duplicates
            return list(dict.fromkeys(cleaned))[:18]
        return []
    except Exception as e:
        print("Keyword Extract Error:", e)
        return []