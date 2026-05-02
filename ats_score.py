def calculate_advanced_ats_score(resume_text, jd_skills, matched_skills):
    if not jd_skills:
        return 0
    resume_text_lower = resume_text.lower()

    #Skill Match (45%)
    
    match_ratio = len(matched_skills) / len(jd_skills)
    skill_score = match_ratio * 100

    #Frequency Score (10%) — controlled

    freq_score = 0
    for skill in matched_skills:
        count = resume_text_lower.count(skill.lower())
        freq_score += min(count * 1.5, 6)  
    freq_score = min(freq_score, 50)  

    #Context Score (10%)

    context_score = 0
    if "project" in resume_text_lower:
        context_score += 6
    if "experience" in resume_text_lower:
        context_score += 4
    
    #Missing Penalty (STRONG)
    
    missing_count = len(jd_skills) - len(matched_skills)
    if missing_count > 0:
        penalty = missing_count * 4
    else:
        penalty = 0
    
    #Base Score(15%)
    
    base_score = 15
    
    #Final Score Calculation
    
    final_score = (
        0.45 * skill_score +
        0.10 * freq_score +
        0.10 * context_score +
        base_score -
        penalty
    )
    
    #Result
    
    final_score = max(0, min(final_score, 100))
    return round(final_score, 2)