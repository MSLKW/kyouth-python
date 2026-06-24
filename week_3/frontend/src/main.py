from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

CURRENT_FILE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = CURRENT_FILE_DIR / Path("templates/chat_page.js")

templates = Jinja2Templates(CURRENT_FILE_DIR / "templates")

@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
	return (templates.TemplateResponse(
		request = request,
		name = "chat_page.html",
	))

@app.get("/chat_page.js")
def get_script():
	with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
		script = f.read()
	return Response(content=script, media_type="text/javascript")