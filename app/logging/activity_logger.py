import os
import csv
from datetime import datetime
from app.models.buyer import BuyerRecord

BUYERS_FILE = "data/buyers.csv"
SENT_LOG_FILE = "data/sent_log.csv"
BUSINESS_EMAILS_FILE = "data/business_emails.csv"
INDIVIDUAL_EMAILS_FILE = "data/individual_emails.csv"
UNKNOWN_EMAILS_FILE = "data/unknown_emails.csv"

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
    _init_csv(UNKNOWN_EMAILS_FILE, ["email"])

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

def append_classified_emails(business_emails: list[str], individual_emails: list[str], unknown_emails: list[str] = None):
    _ensure_dir(BUSINESS_EMAILS_FILE)
    existing_biz = set()
    if os.path.exists(BUSINESS_EMAILS_FILE):
        with open(BUSINESS_EMAILS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            existing_biz = {r[0].strip() for r in reader if r and r[0].strip()}
            
    new_biz = [e for e in (business_emails or []) if e and e.strip() not in existing_biz]
    if new_biz:
        with open(BUSINESS_EMAILS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for e in new_biz:
                writer.writerow([e.strip()])

    _ensure_dir(INDIVIDUAL_EMAILS_FILE)
    existing_ind = set()
    if os.path.exists(INDIVIDUAL_EMAILS_FILE):
        with open(INDIVIDUAL_EMAILS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            existing_ind = {r[0].strip() for r in reader if r and r[0].strip()}
            
    new_ind = [e for e in (individual_emails or []) if e and e.strip() not in existing_ind]
    if new_ind:
        with open(INDIVIDUAL_EMAILS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for e in new_ind:
                writer.writerow([e.strip()])

    if unknown_emails:
        _ensure_dir(UNKNOWN_EMAILS_FILE)
        existing_unk = set()
        if os.path.exists(UNKNOWN_EMAILS_FILE):
            with open(UNKNOWN_EMAILS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                existing_unk = {r[0].strip() for r in reader if r and r[0].strip()}
                
        new_unk = [e for e in unknown_emails if e and e.strip() not in existing_unk]
        if new_unk:
            with open(UNKNOWN_EMAILS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for e in new_unk:
                    writer.writerow([e.strip()])
