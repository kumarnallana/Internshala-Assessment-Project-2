import os
import time
import logging
from typing import List, Tuple
from app.classification.base import BaseClassifier
from app.classification.mock_classifier import MockClassifier

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class GeminiClassifier(BaseClassifier):
    def __init__(self, api_key: str = None, use_mock: bool = False):
        self.use_mock = use_mock
        self.mock = MockClassifier()
        
        if not use_mock:
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                logging.warning("GEMINI_API_KEY not found. Falling back to MockClassifier.")
                self.use_mock = True
            elif not GENAI_AVAILABLE:
                logging.warning("google-generativeai not installed. Falling back to MockClassifier.")
                self.use_mock = True
            else:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')

    def classify_emails(self, emails: List[str]) -> Tuple[List[str], List[str]]:
        if self.use_mock:
            return self.mock.classify_emails(emails)
            
        business_emails = []
        individual_emails = []
        
        # Batch processing: 50 emails per prompt
        batch_size = 50
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            prompt = (
                "You are an AI assistant tasked with classifying a list of emails into 'BUSINESS' or 'INDIVIDUAL'. "
                "Classify emails based on the domain and local part. For example, generic domains like gmail.com or yahoo.com "
                "are usually INDIVIDUAL unless they contain business keywords. Corporate domains are usually BUSINESS.\n"
                "Return exactly the email address, a comma, and the classification label (BUSINESS or INDIVIDUAL), one per line.\n"
                "Do not include any other text.\n\n"
            )
            for e in batch:
                prompt += f"{e}\n"
                
            retries = 3
            for attempt in range(retries):
                try:
                    response = self.model.generate_content(prompt)
                    lines = response.text.strip().split('\n')
                    for line in lines:
                        parts = line.split(',')
                        if len(parts) == 2:
                            email, label = parts[0].strip(), parts[1].strip().upper()
                            if label == 'BUSINESS':
                                business_emails.append(email)
                            else:
                                individual_emails.append(email)
                    break # Success, move to next batch
                except Exception as ex:
                    logging.error(f"Gemini API error: {ex}")
                    time.sleep(2 ** attempt) # Exponential backoff
            else:
                # If all retries fail, fall back to individual or log
                logging.error("Failed to classify batch. Defaulting to INDIVIDUAL.")
                individual_emails.extend(batch)
                
        return business_emails, individual_emails
