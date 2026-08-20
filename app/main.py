from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="NirapodNet")

# Static files (CSS + JavaScript)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/api")
def api_status():
    return {
        "system": "NirapodNet",
        "status": "online"
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )