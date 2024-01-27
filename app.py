from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from contact import Contact


app = FastAPI(default_response_class=HTMLResponse)


@app.get("/")
def index():
    return RedirectResponse("/contacts")


@app.get("/contacts")
def contacts(request: Request):
    query = request.query_params.get("q")

    if not query:
        contacts_set = Contact.search(query)
    else:
        contacts_set = Contact.contacts
