import re

#SKILL DATABASE WITH VARIATIONS

SKILLS_DB = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++"],
    "javascript": ["javascript", "js"],

    "react": ["react", "react.js"],
    "node": ["node", "nodejs", "node.js"],
    "express": ["express", "express.js"],
    "html": ["html"],
    "css": ["css"],

    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],

    "mongodb": ["mongodb"],
    "sql": ["sql"],
    "mysql": ["mysql"],

    "aws": ["aws"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],

    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp"],
    "genai": ["genai", "generative ai"],

    "git": ["git"],
    "github": ["github"],
    "rest api": ["rest api", "restful api", "api", "apis"]
}

#SKILL EXTRACTION FUNCTION
def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    found_skills = set()
    for main_skill, variations in SKILLS_DB.items():
        for variation in variations:
            if re.search(r"\b" + re.escape(variation) + r"\b", text):
                found_skills.add(main_skill)
                break  # stop after first match
    return list(found_skills)