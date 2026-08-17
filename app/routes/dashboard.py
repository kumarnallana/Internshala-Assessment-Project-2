from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.reports.report_generator import generate_summary_report
from app.config import DRY_RUN

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    summary = generate_summary_report()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "summary": summary,
        "dry_run": DRY_RUN
    })
