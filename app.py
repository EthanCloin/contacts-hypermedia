from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(default_response_class=HTMLResponse)


@app.get("/")
def index():
    return "Hello World"
