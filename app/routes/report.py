from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.reports.report_generator import generate_summary_report

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/report", response_class=HTMLResponse)
def report_page(request: Request):
    summary = generate_summary_report()
    return templates.TemplateResponse(request, "report.html", {"request": request, "summary": summary})
