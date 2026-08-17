from typing import List, Tuple
from app.classification.base import BaseClassifier
import logging

class MockClassifier(BaseClassifier):
    def classify_emails(self, emails: List[str]) -> Tuple[List[str], List[str]]:
        """
        Mock implementation.
        In this mock, emails containing 'business', 'sales', 'info', or 'corp' are BUSINESS.
        Others are INDIVIDUAL.
        """
        logging.info(f"Mock classifying {len(emails)} emails")
        business_emails = []
        individual_emails = []
        
        business_keywords = ['business', 'sales', 'info', 'corp']
        
        for email in emails:
            is_business = False
            for kw in business_keywords:
                if kw in email.lower():
                    is_business = True
                    break
            
            if is_business:
                business_emails.append(email)
            else:
                individual_emails.append(email)
                
        return business_emails, individual_emails
