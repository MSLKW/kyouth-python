from fastapi import FastAPI
from prompt_model import prompt_model
import os

app = FastAPI()

@app.post("/chat")
def chat(payload: dict[str, str]):
	prompt = payload["message"]
	try:
		message = prompt_model(os.environ.get("GEMINI_MODEL"), prompt)
	except Exception as e:
		message = "Error occured while prompting model"
	return {"message": message}