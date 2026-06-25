import pydantic
from pathlib import Path
import sqlite3
from prompt_model import prompt_model
import os
import re


class SkillGapResult(pydantic.BaseModel):
    gaps: list[str]


# Returns None on error, Returns SkillGapResult on success
def find_skill_gaps(resume_contents: str, db_url: str) -> SkillGapResult:
    db_path = Path(db_url)
    if not db_path.exists():
        print(f"Database at {db_path} does not exist")
        return None
    if resume_contents == "":
        print(f"Resume contents is empty")
        return None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" 
		SELECT tech_stack FROM jobs WHERE tech_stack != 'N/A' AND tech_stack IS NOT NULL
	""")

    tuple_list = cursor.fetchall()
    flatten_list = [element for tuple in tuple_list for element in tuple]
    tech_dupes = ", ".join(flatten_list).lower()
    tech_list = list(set(tech_dupes.split(", ")))
    tech_list.sort()

    prompt = f"""
    	Examine the resume given and extract the technical skills from the resume.
    	Format the technical skills in this format: tech_skill1,tech_skill2,tech_skill3, ...
        Do not output anything else other than the technical skills.
        The provided resume: {resume_contents}"""
    try:
        tech_skills = prompt_model(os.environ.get("GEMINI_MODEL"), prompt=prompt)
    except Exception:
        print("Error occured during AI prompt")
        return None
    
    data_pattern = r"^[^,]+(?:,\s*[^,]+)*,?$"
    if (bool(re.fullmatch(data_pattern, tech_skills)) == False):
        print(f"AI returned invalid AI Output: {tech_skills}")
        return None
        
    resume_skills_list = tech_skills.lower().split(", ")

    missing_skills = tech_list
    for skill in resume_skills_list:
        if skill in missing_skills:
            missing_skills.remove(skill)

    skill_gap_result = SkillGapResult(gaps=missing_skills)
    return skill_gap_result

