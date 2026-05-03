from fastapi import FastAPI, UploadFile, File, Form
import asyncio

from resume_parser import extract_resume_text
from jd_parser import extract_jd_text

from skill_extractor import extract_skills
from keyword_extractor import extract_keywords
from ai_keyword_extractor import extract_keywords_ai
from ai_skill_extractor import extract_skills_ai

from matcher import match_skills
from ats_score import calculate_advanced_ats_score
from llm_rewriter import rewrite_resume_sections

from visualizer import create_ats_bar_chart, create_pie_chart


app = FastAPI()

cache = {}

def cached_call(key, func, *args):
    if key in cache:
        return cache[key]
    result = func(*args)
    cache[key] = result
    return result

async def run_in_thread(func, *args):
    return await asyncio.to_thread(func, *args)


# Filter keywords
def filter_keywords(keywords):
    valid = []
    for k in keywords:
        k = k.lower().strip()

        if len(k.split()) > 2:
            continue

        if any(x in k for x in ["engineer", "developer", "sde"]):
            continue

        if any(x in k for x in [
            "react", "node", "mongodb", "docker", "aws",
            "ci/cd", "api", "express", "mysql", "git"
        ]):
            valid.append(k)

    return list(dict.fromkeys(valid))


# Normalize skill names
def normalize_skill(skill):
    skill = skill.lower().strip()

    mapping = {
        "nodejs": "node",
        "node.js": "node",
        "expressjs": "express",
        "express.js": "express",
        "react.js": "react",
        "restapi": "rest api",
        "rest": "rest api",
        "api": "rest api",
        "restful apis": "rest api",
        "mongod": "mongodb",
        "cicd": "ci/cd",
        "pipelines": "ci/cd",
        "mysql": "sql",
        "containerization": "docker",
        "git/github": "git"
    }

    return mapping.get(skill, skill)


def clean_keyword(k):
    k = k.lower().strip()

    replacements = {
        "restapi": "rest api",
        "node.js": "node",
        "express.js": "express",
        "react.js": "react",
        "pipelines": "ci/cd",
        "containerization": "docker"
    }

    blacklist = {"fundamentals", "basic", "knowledge"}

    if k in blacklist:
        return ""

    return replacements.get(k, k)


def unique_list(lst):
    return list(dict.fromkeys([x for x in lst if x]))


@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(None),
    jd_file: UploadFile = File(None)
):

    # Extract resume
    resume_text = await extract_resume_text(resume)

    # Extract JD
    if job_description:
        jd_text = job_description
    elif jd_file:
        jd_text = await extract_jd_text(jd_file)
    else:
        return {"error": "Provide job_description or jd_file"}

    if not jd_text or len(jd_text.strip()) < 50:
        return {"error": "JD extraction failed"}

    # Run AI tasks
    jd_skills_task = run_in_thread(
        cached_call, jd_text+"_skills", extract_skills_ai, jd_text
    )

    jd_keywords_task = run_in_thread(
        cached_call, jd_text+"_keywords", extract_keywords_ai, jd_text
    )

    jd_skill_data, jd_keywords = await asyncio.gather(
        jd_skills_task, jd_keywords_task
    )

    # Resume skills
    # after extracting resume_skills

    resume_skills = unique_list([
        normalize_skill(s) for s in extract_skills(resume_text)
    ])


    # infer backend skills
    if "api" in resume_text.lower():
        resume_skills.append("node")

    if "rest api" in resume_text.lower():
        resume_skills.append("express")

    resume_skills = unique_list(resume_skills)

    # JD skills
    must_have_skills = unique_list([
        normalize_skill(s) for s in jd_skill_data.get("must_have", [])
    ])

    good_to_have_skills = unique_list([
        normalize_skill(s) for s in jd_skill_data.get("good_to_have", [])
    ])

    # Keywords
    if not jd_keywords or len(jd_keywords) < 10:
        jd_keywords = extract_keywords(jd_text)

    jd_keywords = filter_keywords([
        normalize_skill(clean_keyword(s))
        for s in jd_keywords
        if clean_keyword(s)
    ])

    # Combine JD skills
    all_jd_skills = unique_list(
        must_have_skills + good_to_have_skills + jd_keywords
    )

    # Match skills
    matched_all, missing_all = match_skills(resume_skills, all_jd_skills)

    matched_all = unique_list(matched_all)
    missing_all = unique_list(missing_all)

    # ATS before
    ats_score_before = calculate_advanced_ats_score(
        resume_text, all_jd_skills, matched_all
    )

    # Rewrite resume
    rewritten_resume = await run_in_thread(
        cached_call,
        resume_text[:300] + "_rewrite",
        rewrite_resume_sections,
        resume_text[:400],
        jd_text[:1000],
        missing_all
    )

    # Updated skills
    updated_resume_skills = unique_list([
        normalize_skill(s) for s in extract_skills(rewritten_resume)
    ])

    # add detected keywords from rewritten resume
    for skill in all_jd_skills:
        if skill in rewritten_resume.lower():
            updated_resume_skills.append(skill)

    updated_resume_skills = unique_list(updated_resume_skills)

    for kw in jd_keywords:
        if kw in rewritten_resume.lower():
            updated_resume_skills.append(kw)

    updated_resume_skills = unique_list(updated_resume_skills)

    updated_matched_all, _ = match_skills(
        updated_resume_skills, all_jd_skills
    )

    # ATS after
    raw_ats_after = calculate_advanced_ats_score(
        rewritten_resume, all_jd_skills, updated_matched_all
    )

    ats_score_after = max(
        ats_score_before,
        min(raw_ats_after, ats_score_before + 20, 92)
    )

    # Charts
    ats_chart = create_ats_bar_chart(ats_score_before, ats_score_after)
    jd_chart = create_pie_chart("JD Keywords", jd_keywords)
    resume_chart = create_pie_chart("Resume Skills", resume_skills)
    
    # Suggestions
    suggestions = [
        f"Add or improve experience in {s}"
        for s in missing_all
        if len(s.split()) <= 2 and not any(x in s for x in ["engineer", "developer"])
    ]

    # Response
    return {
        "resume_preview": resume_text[:300],
        "jd_keywords": jd_keywords,

        "resume_skills": resume_skills,

        "must_have_skills": must_have_skills,
        "good_to_have_skills": good_to_have_skills,

        "matched_skills": matched_all,
        "missing_skills": missing_all,

        "ats_score_before": ats_score_before,
        "ats_score_after": ats_score_after,

        "charts": {
            "ats_bar": ats_chart,
            "jd_keywords_pie": jd_chart,
            "resume_pie": resume_chart
        },

        "suggestions": suggestions,
        "rewritten_resume": rewritten_resume
    }