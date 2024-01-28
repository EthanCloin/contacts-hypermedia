from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks

from contacts import Contact

Contact.load_db()
APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
templates = Jinja2Blocks(TEMPLATE_DIR)
app = FastAPI(default_response_class=HTMLResponse)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return RedirectResponse("/contacts")


@app.get("/contacts")
def contacts(request: Request):
    query = request.query_params.get("q")

    if query:
        contacts_set = Contact.search(query)
    else:
        contacts_set = Contact.all()

    return templates.TemplateResponse(
        "index.html", {"request": request, "contacts": contacts_set}
    )
