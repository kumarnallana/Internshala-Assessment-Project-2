from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.pipeline import PipelineService
from app.config import SEARCH_KEYWORD

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/upload")
def run_discovery():
    pipeline = PipelineService(keyword=SEARCH_KEYWORD)
    total, valid = pipeline.run_discovery()
    return RedirectResponse(url="/?msg=discovery_complete", status_code=303)
