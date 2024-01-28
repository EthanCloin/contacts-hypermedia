from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from jinja2_fragments.fastapi import Jinja2Blocks
from starlette.middleware.sessions import SessionMiddleware
from contacts import Contact
import secrets


Contact.load_db()
APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
secret_key = secrets.token_urlsafe(32)
templates = Jinja2Blocks(TEMPLATE_DIR)

app = FastAPI(default_response_class=HTMLResponse)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.add_middleware(SessionMiddleware, secret_key=secret_key)


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


@app.get("/contacts/new")
def contacts_new_get(request: Request):
    return templates.TemplateResponse(
        "new.html", {"request": request, "contact": Contact()}
    )


@app.post("/contacts/new")
async def contacts_new(request: Request, response: Response):
    form = await request.form()
    c = Contact(
        None, form["first_name"], form["last_name"], form["phone"], form["email"]
    )

    if c.save():
        request.session["message"] = "Created New Contact!"
        return RedirectResponse("/contacts", status_code=301)
    else:
        return templates.TemplateResponse(
            "new.html", {"request": request, "contact": c}
        )
