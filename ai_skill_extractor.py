import subprocess
import json
import re

def extract_skills_ai(text):
    prompt = f"""
Extract skills from this job description.

Return ONLY valid JSON.

STRICT FORMAT:
{{
  "must_have": ["skill1", "skill2"],
  "good_to_have": ["skill3", "skill4"]
}}

RULES:
- No explanation
- No text outside JSON
- Must include at least 3 skills in each list

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
        print("\n--- RAW SKILL OUTPUT ---\n", output, "\n")
        match = re.search(r"\{[\s\S]*\}", output)
        if match:
            try:
                data = json.loads(match.group(0))
                must_have = [
                    s.lower().strip()
                    for s in data.get("must_have", [])
                    if len(s) > 2
                ]
                good_to_have = [
                    s.lower().strip()
                    for s in data.get("good_to_have", [])
                    if len(s) > 2
                ]
                if must_have or good_to_have:
                    return {
                        "must_have": list(set(must_have)),
                        "good_to_have": list(set(good_to_have))
                    }
            except Exception as e:
                print("JSON parsing failed:", e)
        fallback_must = ["react", "node", "mongodb"]
        fallback_good = ["docker", "aws", "ci/cd"]
        return {
            "must_have": fallback_must,
            "good_to_have": fallback_good
        }
    except Exception as e:
        print("AI Skill Extract Error:", e)
        return {
            "must_have": ["react", "node", "mongodb"],
            "good_to_have": ["docker", "aws"]
        }