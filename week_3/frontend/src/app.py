from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates("templates")

@app.get('/', response_class=HTMLResponse)
def get_root(request: Request):
	return (templates.TemplateResponse(
		request = request,
		name = "chat_page.html",
	))