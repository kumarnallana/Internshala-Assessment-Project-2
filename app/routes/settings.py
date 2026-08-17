from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import GMAIL_EMAIL, DRY_RUN

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "email": GMAIL_EMAIL, "dry_run": DRY_RUN})
