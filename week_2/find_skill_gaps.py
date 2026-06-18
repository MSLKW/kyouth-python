import pydantic
from pathlib import Path
import sqlite3


class SkillGapResult(pydantic.BaseModel):
    gaps: list[str]


# Returns None on error, Returns SkillGapResult on success
def find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult:
    db_path = Path(db_url)
    resume_file = Path(input_file_path)
    if not db_path.exists():
        print(f"Database at {db_path} does not exist")
        return None
    if not resume_file.exists():
        print(f"Resume file at {resume_file} does not exist")
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

    with open(resume_file, "r", encoding="utf-8") as f:
        resume_contents = f.read()

    keyword = "Technical Skills:"
    keyword_index = resume_contents.find(keyword)
    if keyword_index == -1:
        print("Could not find technical skills in resume")
        return None
    keyword_index += len(keyword)
    new_line_index = resume_contents.find("\n", keyword_index)
    if new_line_index == -1:
        print("Could not complete search for technical skills in resume")
        return None
    tech_skills = resume_contents[keyword_index:new_line_index]
    resume_skills_list = tech_skills.lower().split(", ")

    missing_skills = tech_list
    for skill in resume_skills_list:
        if skill in missing_skills:
            missing_skills.remove(skill)

    skill_gap_result = SkillGapResult(gaps=missing_skills)
    return skill_gap_result


if __name__ == "__main__":
    skill_gap_result = find_skill_gaps("data/resume_d3.txt", "data/jobs_d1.db")
    if skill_gap_result is not None:
        print(f"gaps={skill_gap_result.gaps}")
