from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.pipeline import PipelineService
from app.config import SEARCH_KEYWORD
from app.classification.gemini_classifier import GeminiClassifier

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/classify", response_class=HTMLResponse)
def classify_page(request: Request):
    return templates.TemplateResponse(request, "classify.html", {"request": request})

@router.post("/classify")
def run_classification():
    pipeline = PipelineService(keyword=SEARCH_KEYWORD)
    classifier = GeminiClassifier()
    b, i, u = pipeline.run_classification(classifier)
    return RedirectResponse(url="/?msg=classification_complete", status_code=303)
