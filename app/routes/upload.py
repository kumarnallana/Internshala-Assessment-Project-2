from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.pipeline import PipelineService
from app.config import SEARCH_KEYWORD

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse(request, "upload.html", {"request": request, "keyword": SEARCH_KEYWORD})

@router.post("/upload")
def run_discovery(keyword: str = Form(None)):
    kw = keyword.strip() if keyword and keyword.strip() else SEARCH_KEYWORD
    pipeline = PipelineService(keyword=kw, use_mock=False)
    total, valid = pipeline.run_discovery()
    return RedirectResponse(url="/?msg=discovery_complete", status_code=303)
