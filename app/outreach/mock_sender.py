import logging
from typing import List
from app.outreach.base import BaseSender
from app.logging.activity_logger import log_send_attempt, get_sent_log

class MockSender(BaseSender):
    def send_campaign(self, emails: List[str], subject: str, body: str, attachment_path: str = None) -> tuple[int, int, List[str], List[str], List[str]]:
        logging.info("Starting Mock Campaign")
        success_count = 0
        failed_count = 0
        successful = []
        failed = []
        skipped = []
        
        sent_log = get_sent_log()
        previously_sent = {row["email"] for row in sent_log if row["status"] == "sent"}

        for email in emails:
            if email in previously_sent:
                logging.info(f"Skipping {email} (already sent)")
                log_send_attempt(email, "skipped_duplicate")
                skipped.append(email)
                continue
                
            logging.info(f"[MOCK SEND] To: {email} | Subject: {subject} | Attachment: {attachment_path}")
            log_send_attempt(email, "sent")
            success_count += 1
            successful.append(email)
            
        return success_count, failed_count, successful, failed, skipped
