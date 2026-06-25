from fastapi import FastAPI
from prompt_model import prompt_model
from find_skill_gaps import find_skill_gaps
import os
from google.genai import errors

app = FastAPI()

@app.post("/chat")
async def chat(payload: dict[str, str]):
	prompt = "Do not use markdown formatting in your response. "
	prompt += payload["message"]
	file_contents = payload["file_contents"]

	if (prompt == "find skill gaps"):
		skill_gaps = find_skill_gaps(file_contents, "data/jobs_d1.db")
		if (skill_gaps is None):
			message = "Error occured while finding skill gaps"
		else:
			message = ", ".join(skill_gaps.gaps)
		return {"message": message}
	else:
		if (file_contents):
			prompt += f"binary_file_contents: {file_contents}"
		try:
			message = prompt_model(os.environ.get("GEMINI_MODEL"), f"{prompt}")
		except errors.APIError as e:
			error_string = str(e)
			message = f"Error occured while prompting model: {error_string}"
		except Exception as e:
			message = "Error occured while prompting model"
		return {"message": message}