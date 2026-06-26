from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import httpx
import os

app = FastAPI()

CURRENT_FILE_DIR = Path(__file__).resolve().parent
SCRIPT_PATH = CURRENT_FILE_DIR / Path("templates/")

templates = Jinja2Templates(CURRENT_FILE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat_page.html",
    )


@app.get("/chat_page.js")
def get_script():
    with open(SCRIPT_PATH / "chat_page.js", "r", encoding="utf-8") as f:
        script = f.read()
    return Response(content=script, media_type="text/javascript")


@app.get("/pdf.mjs")
def get_script_pdf():
    with open(SCRIPT_PATH / "pdf.mjs", "r", encoding="utf-8") as f:
        script = f.read()
    return Response(content=script, media_type="text/javascript")


@app.get("/pdf.worker.mjs")
def get_script_worker():
    with open(SCRIPT_PATH / "pdf.worker.mjs", "r", encoding="utf-8") as f:
        script = f.read()
    return Response(content=script, media_type="text/javascript")


@app.post("/chat")
async def chat(payload: dict[str, str]):
    client = httpx.AsyncClient(base_url=os.environ.get("BACKEND_URL"), timeout=None)
    try:
        response = await client.post("/chat", json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return HTTPException(
            status_code=e.response.status_code,
            detail="Error occured during backend HTTP call",
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Backend is unreachable")
