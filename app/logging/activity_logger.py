import os
import csv
from datetime import datetime
from app.models.buyer import BuyerRecord

BUYERS_FILE = "data/buyers.csv"
SENT_LOG_FILE = "data/sent_log.csv"
BUSINESS_EMAILS_FILE = "data/business_emails.csv"
INDIVIDUAL_EMAILS_FILE = "data/individual_emails.csv"

def _ensure_dir(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

def _init_csv(filepath, fieldnames):
    _ensure_dir(filepath)
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

def init_logs():
    _init_csv(BUYERS_FILE, ["email", "buyer_name", "company_name", "website", "country", "source_platform"])
    _init_csv(SENT_LOG_FILE, ["email", "status", "timestamp", "campaign_id"])
    _init_csv(BUSINESS_EMAILS_FILE, ["email"])
    _init_csv(INDIVIDUAL_EMAILS_FILE, ["email"])

def append_buyers(buyers: list[BuyerRecord]):
    _ensure_dir(BUYERS_FILE)
    with open(BUYERS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["email", "buyer_name", "company_name", "website", "country", "source_platform"])
        for b in buyers:
            writer.writerow(b.to_dict())

def log_send_attempt(email: str, status: str, campaign_id: str = ""):
    _ensure_dir(SENT_LOG_FILE)
    with open(SENT_LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([email, status, datetime.utcnow().isoformat(), campaign_id])

def get_sent_log():
    if not os.path.exists(SENT_LOG_FILE):
        return []
    with open(SENT_LOG_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def append_classified_emails(business_emails: list[str], individual_emails: list[str]):
    _ensure_dir(BUSINESS_EMAILS_FILE)
    if business_emails:
        with open(BUSINESS_EMAILS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for e in business_emails:
                writer.writerow([e])
                
    _ensure_dir(INDIVIDUAL_EMAILS_FILE)
    if individual_emails:
        with open(INDIVIDUAL_EMAILS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for e in individual_emails:
                writer.writerow([e])
