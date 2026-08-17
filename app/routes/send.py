from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import csv
from app.config import DRY_RUN, PRESENTATION_PATH
from app.outreach.gmail_sender import GmailSender

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/send", response_class=HTMLResponse)
def send_page(request: Request):
    return templates.TemplateResponse(request, "send.html", {"request": request, "dry_run": DRY_RUN})

@router.post("/send")
def run_send(audience: str = Form(...), subject: str = Form(...), body: str = Form(...)):
    emails = []
    files_to_read = []
    
    if audience == "business":
        files_to_read.append("data/business_emails.csv")
    elif audience == "individual":
        files_to_read.append("data/individual_emails.csv")
    else:
        files_to_read = ["data/buyers.csv"]
        
    for f in files_to_read:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                reader = csv.reader(fh)
                next(reader, None)  # Skip header row in any CSV
                for row in reader:
                    if row and row[0]:
                        emails.append(row[0].strip())
        except FileNotFoundError:
            pass
            
    emails = list(set(emails))
    sender = GmailSender()
    sender.send_campaign(emails, subject, body, PRESENTATION_PATH)
    return RedirectResponse(url="/report", status_code=303)
