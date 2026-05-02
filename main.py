from fastapi import FastAPI, UploadFile, File, Form
import asyncio
from resume_parser import extract_resume_text
from jd_parser import extract_jd_text
from skill_extractor import extract_skills
from keyword_extractor import extract_keywords
from ai_skill_extractor import extract_skills_ai
from matcher import match_skills
from ats_score import calculate_advanced_ats_score
from llm_rewriter import rewrite_resume_sections

app = FastAPI()

cache = {}  # Simple in-memory cache

def cached_call(key, func, *args):
    if key in cache:
        return cache[key]
    result = func(*args)
    cache[key] = result
    return result

async def run_in_thread(func, *args):
    return await asyncio.to_thread(func, *args)

@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(None),
    jd_file: UploadFile = File(None)
):
    #Resume Extraction
    resume_text = await extract_resume_text(resume)
    
    #JD Extraction
    if job_description:
        jd_text = job_description
    elif jd_file:
        jd_text = await extract_jd_text(jd_file)
    else:
        return {"error": "Provide job_description or jd_file"}
    if not jd_text or len(jd_text.strip()) < 50:
        return {"error": "JD extraction failed or too short"}
    print("\n===== JD TEXT =====\n", jd_text[:500], "\n=================\n")

    #PARALLEL SKILL EXTRACTION
    jd_skills_task = run_in_thread(
        cached_call,
        jd_text + "_skills",
        extract_skills_ai,
        jd_text
    )
    jd_skill_data = await jd_skills_task

    #Resume Skills
    resume_skills = extract_skills(resume_text)
    must_have_skills = jd_skill_data.get("must_have", [])
    good_to_have_skills = jd_skill_data.get("good_to_have", [])
    
    #Keywords(NO LLM)
    jd_keywords = list(set(must_have_skills + good_to_have_skills))
    if not jd_keywords:
        jd_keywords = extract_keywords(jd_text)
    
    #Matching
    all_jd_skills = list(set(must_have_skills + good_to_have_skills))
    matched_skills, missing_skills = match_skills(
        resume_skills,
        all_jd_skills
    )
    
    #ATS BEFORE
    ats_score_before = calculate_advanced_ats_score(
        resume_text,
        must_have_skills,
        matched_skills
    )

    #REWRITE resume(AFTER MATCHING)
    rewritten_resume = await run_in_thread(
        cached_call,
        resume_text[:300] + "_rewrite",
        rewrite_resume_sections,
        resume_text[:400],
        jd_text[:300],
        missing_skills
    )

    #ATS AFTER
    updated_resume_skills = extract_skills(rewritten_resume)
    updated_matched_skills, _ = match_skills(
        updated_resume_skills,
        all_jd_skills
    )
    raw_ats_after = calculate_advanced_ats_score(
        rewritten_resume,
        must_have_skills,
        updated_matched_skills
    )
    max_increase = 20  # cap improvement
    ats_score_after = min(
        ats_score_before + max_increase,
        raw_ats_after,
        92  # hard upper limit
    )
    
    #Suggestions
    suggestions = [
        f"Add or improve experience in {skill}"
        for skill in missing_skills
    ]

    #Final Response
    return {
        "resume_preview": resume_text[:300],
        "jd_keywords": jd_keywords,
        "resume_skills": resume_skills,
        "must_have_skills": must_have_skills,
        "good_to_have_skills": good_to_have_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score_before": ats_score_before,
        "ats_score_after": ats_score_after,
        "suggestions": suggestions,
        "rewritten_resume": rewritten_resume
    }