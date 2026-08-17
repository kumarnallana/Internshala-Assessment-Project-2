import csv
import io
from app.logging.activity_logger import BUYERS_FILE, SENT_LOG_FILE, BUSINESS_EMAILS_FILE, INDIVIDUAL_EMAILS_FILE

def get_line_count(filepath: str) -> int:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0

def generate_summary_report() -> dict:
    buyers_count = max(0, get_line_count(BUYERS_FILE) - 1) # minus header
    business_count = get_line_count(BUSINESS_EMAILS_FILE)
    individual_count = get_line_count(INDIVIDUAL_EMAILS_FILE)
    
    sent_log_count = max(0, get_line_count(SENT_LOG_FILE) - 1)
    
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    try:
        with open(SENT_LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                st = row.get("status", "")
                if st == "sent":
                    success_count += 1
                elif st == "failed" or st == "failed_attachment":
                    failed_count += 1
                elif st == "skipped_duplicate":
                    skipped_count += 1
    except FileNotFoundError:
        pass
        
    return {
        "total_buyers": buyers_count,
        "business_classified": business_count,
        "individual_classified": individual_count,
        "total_send_attempts": success_count + failed_count + skipped_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "skipped_count": skipped_count
    }

def generate_csv_report() -> str:
    summary = generate_summary_report()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Metric", "Value"])
    for k, v in summary.items():
        writer.writerow([k, v])
        
    writer.writerow([])
    writer.writerow(["Email", "Status", "Timestamp"])
    
    try:
        with open(SENT_LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None) # skip header
            for row in reader:
                writer.writerow(row)
    except FileNotFoundError:
        pass
        
    return output.getvalue()
