from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

CURRENT_FILE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(CURRENT_FILE_DIR / "templates")

@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
	return (templates.TemplateResponse(
		request = request,
		name = "chat_page.html",
	))