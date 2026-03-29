import re

SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "sql", "mongodb", "fastapi", "django", "flask",
    "data analysis", "nlp", "cloud", "aws", "docker"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return list(set(found_skills))