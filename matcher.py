def normalize_skill(skill):
    return skill.lower().strip()

def match_skills(resume_skills, jd_skills):
    # Normalize skills
    resume_set = set(normalize_skill(s) for s in resume_skills)
    jd_set = set(normalize_skill(s) for s in jd_skills)
    matched = []
    missing = []
    for jd_skill in jd_set:
        found = False
        for res_skill in resume_set:
            # Exact match
            if jd_skill == res_skill:
                found = True
                break
            #Partial match(react vs react.js, node vs nodejs)
            if jd_skill in res_skill or res_skill in jd_skill:
                found = True
                break
        if found:
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)
    return matched, missing