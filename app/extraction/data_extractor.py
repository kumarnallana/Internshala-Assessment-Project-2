import re
from typing import List
from app.models.buyer import BuyerRecord

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

def extract_emails_from_text(text: str) -> List[str]:
    """Extracts raw candidate emails from unstructured text."""
    if not text:
        return []
    candidates = set(EMAIL_PATTERN.findall(text))
    valid_candidates = []
    
    for e in candidates:
        e = e.strip().lower().rstrip('.')
        if e.endswith(IMAGE_EXTENSIONS) or any(ext + '@' in e for ext in IMAGE_EXTENSIONS):
            continue
            
        parts = e.split('@')
        if len(parts) == 2 and len(parts[1]) > 50:
            continue
            
        valid_candidates.append(e)
        
    return valid_candidates

def create_buyer_records_from_data(
    raw_text: str, 
    buyer_name: str = "", 
    company_name: str = "", 
    website: str = "", 
    country: str = "", 
    source_platform: str = ""
) -> List[BuyerRecord]:
    """
    Extracts emails from text and returns normalized BuyerRecords.
    If no email is found, returns a record with an empty email (for manual review).
    """
    emails = extract_emails_from_text(raw_text)
    records = []
    
    if not emails:
        # Create a placeholder record for review
        records.append(BuyerRecord(
            email="",
            buyer_name=buyer_name.strip(),
            company_name=company_name.strip(),
            website=website.strip(),
            country=country.strip(),
            source_platform=source_platform.strip()
        ))
    else:
        for e in emails:
            records.append(BuyerRecord(
                email=e,
                buyer_name=buyer_name.strip(),
                company_name=company_name.strip(),
                website=website.strip(),
                country=country.strip(),
                source_platform=source_platform.strip()
            ))
            
    return records
