import re
import logging

# We use the regex-based validation for syntax from the spec.
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

INVALID_PLACEHOLDERS = [
    "example.com", "yourdomain.com", "email.com", "test.com", "domain.com",
    "placeholder", "noreply", "no-reply"
]

def is_valid_syntax(email: str) -> bool:
    if not email:
        return False
    if not EMAIL_REGEX.fullmatch(email):
        return False
    return True

def is_placeholder(email: str) -> bool:
    lower_email = email.lower()
    for ph in INVALID_PLACEHOLDERS:
        if ph in lower_email:
            return True
    return False

def validate_email(email: str) -> str:
    """
    Returns 'VALID', 'INVALID', or 'REVIEW_REQUIRED'.
    """
    if not email or not email.strip():
        return "REVIEW_REQUIRED"
    
    email = email.strip()
    
    if not is_valid_syntax(email):
        return "INVALID"
        
    if is_placeholder(email):
        return "INVALID"
        
    return "VALID"

def filter_buyers_for_queue(buyers: list) -> tuple[list, list]:
    """
    Takes a list of BuyerRecords and splits them into valid queueable buyers and ones requiring review/invalid.
    """
    valid_queue = []
    invalid_or_review = []
    
    for b in buyers:
        status = validate_email(b.email)
        if status == "VALID":
            valid_queue.append(b)
        else:
            logging.info(f"Buyer {b.email} excluded. Status: {status}")
            invalid_or_review.append((b, status))
            
    return valid_queue, invalid_or_review
