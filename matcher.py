def normalize_skill(skill):
    skill = skill.lower().strip()

    mapping = {
        "nodejs": "node",
        "node.js": "node",
        "expressjs": "express",
        "express.js": "express",
        "react.js": "react",
        "restapi": "rest api",
        "restful apis": "rest api",
        "rest": "rest api",
        "api": "rest api",
        "mongod": "mongodb",
        "cicd": "ci/cd",
        "pipelines": "ci/cd",
        "containerization": "docker"
    }

    return mapping.get(skill, skill)


def match_skills(resume_skills, jd_skills):

    resume_set = set(normalize_skill(s) for s in resume_skills)
    jd_set = set(normalize_skill(s) for s in jd_skills)

    matched = []
    missing = []

    for jd in jd_set:
        found = False
        for r in resume_set:
            if jd == r:
                found = True
                break
            if jd in r or r in jd:
                found = True
                break

        if found:
            matched.append(jd)
        else:
            missing.append(jd)

    return list(set(matched)), list(set(missing))