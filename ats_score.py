def calculate_advanced_ats_score(resume_text, jd_skills, matched_skills):
    if not jd_skills:
        return 0

    resume_text_lower = resume_text.lower()

    # Skill match
    match_ratio = len(matched_skills) / len(jd_skills)
    skill_score = match_ratio * 100

    # Frequency
    freq_score = 0
    for skill in matched_skills:
        count = resume_text_lower.count(skill.lower())
        freq_score += min(count * 2.5, 10)

    freq_score = min(freq_score, 70)

    # Context
    context_score = 0

    if "project" in resume_text_lower:
        context_score += 4

    if "experience" in resume_text_lower:
        context_score += 3

    if "developed" in resume_text_lower or "built" in resume_text_lower:
        context_score += 2

    if "api" in resume_text_lower:
        context_score += 1

    if "database" in resume_text_lower:
        context_score += 1

    context_score = min(context_score, 10)

    # Penalty
    missing_count = len(jd_skills) - len(matched_skills)
    penalty = missing_count * 2 if missing_count > 0 else 0

    # Base
    base_score = 22

    # Final
    final_score = (
        0.45 * skill_score +
        0.10 * freq_score +
        0.10 * context_score +
        base_score -
        penalty
    )

    return round(max(0, min(final_score, 100)), 2)