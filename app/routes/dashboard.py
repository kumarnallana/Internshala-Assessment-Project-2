import csv
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.reports.report_generator import generate_summary_report
from app.config import DRY_RUN, SEARCH_KEYWORD

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    summary = generate_summary_report()
    
    # Read classified sets for badge rendering
    biz_set = set()
    if os.path.exists("data/business_emails.csv"):
        with open("data/business_emails.csv", "r", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)
            biz_set = {row[0].strip() for row in r if row and row[0].strip()}
            
    ind_set = set()
    if os.path.exists("data/individual_emails.csv"):
        with open("data/individual_emails.csv", "r", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)
            ind_set = {row[0].strip() for row in r if row and row[0].strip()}
            
    sent_map = {}
    if os.path.exists("data/sent_log.csv"):
        with open("data/sent_log.csv", "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                em = row.get("email", "").strip()
                if em:
                    sent_map[em] = row.get("status", "sent")
                    
    # Read all buyers
    buyers = []
    if os.path.exists("data/buyers.csv"):
        with open("data/buyers.csv", "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                email = row.get("email", "").strip()
                category = "Pending"
                if email in biz_set:
                    category = "Business"
                elif email in ind_set:
                    category = "Individual"
                    
                status = sent_map.get(email, "Queued" if email else "No Email")
                buyers.append({
                    "buyer_name": row.get("buyer_name", "") or "N/A",
                    "company_name": row.get("company_name", "") or "N/A",
                    "email": email or "(Needs Review)",
                    "website": row.get("website", ""),
                    "country": row.get("country", "") or "Global",
                    "source_platform": row.get("source_platform", "") or "Web",
                    "category": category,
                    "status": status
                })
                
    return templates.TemplateResponse(request, "dashboard.html", {
        "request": request, 
        "summary": summary,
        "dry_run": DRY_RUN,
        "search_keyword": SEARCH_KEYWORD,
        "buyers": buyers,
        "msg": request.query_params.get("msg")
    })
