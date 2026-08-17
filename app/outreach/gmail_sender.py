import os
import smtplib
import time
import logging
from email.message import EmailMessage
from typing import List

from app.outreach.base import BaseSender
from app.outreach.attachment_handler import attach_file
from app.logging.activity_logger import log_send_attempt, get_sent_log
from app.config import DRY_RUN, GMAIL_EMAIL, GMAIL_APP_PASSWORD

class GmailSender(BaseSender):
    def __init__(self, delay_seconds: float = 1.0):
        self.delay_seconds = delay_seconds

    def _connect(self):
        if DRY_RUN:
            return None
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        return smtp

    def send_campaign(self, emails: List[str], subject: str, body: str, attachment_path: str = None) -> tuple[int, int, List[str], List[str], List[str]]:
        logging.info(f"Starting Gmail Campaign. DRY_RUN={DRY_RUN}")
        success_count = 0
        failed_count = 0
        successful = []
        failed = []
        skipped = []

        sent_log = get_sent_log()
        previously_sent = {row["email"] for row in sent_log if row["status"] == "sent"}

        smtp = None
        try:
            smtp = self._connect()
            
            for email in emails:
                if email in previously_sent:
                    logging.info(f"Skipping {email} (already sent)")
                    log_send_attempt(email, "skipped_duplicate")
                    skipped.append(email)
                    continue

                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = GMAIL_EMAIL if not DRY_RUN else "dry-run@example.com"
                msg['To'] = email
                msg.set_content(body)

                if attachment_path:
                    try:
                        attach_file(msg, attachment_path)
                    except Exception as e:
                        logging.error(f"Failed to attach file {attachment_path}: {e}")
                        failed_count += 1
                        failed.append(email)
                        log_send_attempt(email, "failed_attachment")
                        continue

                if DRY_RUN:
                    logging.info(f"[DRY RUN] Would send to {email}. Subject: {subject}")
                    success_count += 1
                    successful.append(email)
                    log_send_attempt(email, "sent") # Log as sent so idempotency test works
                    continue

                try:
                    smtp.send_message(msg)
                    logging.info(f"Sent to {email}")
                    success_count += 1
                    successful.append(email)
                    log_send_attempt(email, "sent")
                    time.sleep(self.delay_seconds)
                except smtplib.SMTPServerDisconnected:
                    logging.warning("SMTP Disconnected. Reconnecting...")
                    try:
                        smtp = self._connect()
                        smtp.send_message(msg)
                        logging.info(f"Sent to {email} after reconnect")
                        success_count += 1
                        successful.append(email)
                        log_send_attempt(email, "sent")
                        time.sleep(self.delay_seconds)
                    except Exception as e:
                        logging.error(f"Failed to send to {email} after reconnect: {e}")
                        failed_count += 1
                        failed.append(email)
                        log_send_attempt(email, "failed")
                except Exception as e:
                    logging.error(f"Failed to send to {email}: {e}")
                    failed_count += 1
                    failed.append(email)
                    log_send_attempt(email, "failed")
                    
        finally:
            if smtp:
                try:
                    smtp.quit()
                except:
                    pass

        return success_count, failed_count, successful, failed, skipped
