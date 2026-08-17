import logging
from typing import List
from app.search.google_search import GoogleSearchAdapter
from app.search.facebook_search import FacebookSearchAdapter
from app.search.linkedin_search import LinkedInSearchAdapter
from app.search.directory_search import DirectorySearchAdapter
from app.search.website_search import WebsiteSearchAdapter
from app.extraction.data_extractor import create_buyer_records_from_data
from app.validation.email_validator import filter_buyers_for_queue
from app.logging.activity_logger import append_buyers, append_classified_emails

class PipelineService:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.adapters = [
            GoogleSearchAdapter(use_mock=True),
            FacebookSearchAdapter(use_mock=True),
            LinkedInSearchAdapter(use_mock=True),
            DirectorySearchAdapter(use_mock=True),
            WebsiteSearchAdapter(use_mock=True),
        ]

    def run_discovery(self):
        logging.info("Starting Buyer Discovery Phase")
        all_buyers = []
        for adapter in self.adapters:
            results = adapter.search(self.keyword)
            for res in results:
                records = create_buyer_records_from_data(
                    raw_text=res.get("raw_text", ""),
                    buyer_name=res.get("buyer_name", ""),
                    company_name=res.get("company_name", ""),
                    website=res.get("website", ""),
                    country=res.get("country", ""),
                    source_platform=res.get("source_platform", "")
                )
                all_buyers.extend(records)
                
        # Validate and filter
        valid_queue, review_queue = filter_buyers_for_queue(all_buyers)
        
        # Save all to buyers.csv (both valid and invalid/review)
        append_buyers(all_buyers)
        
        logging.info(f"Discovery Complete. Found {len(valid_queue)} valid, {len(review_queue)} review/invalid.")
        return len(all_buyers), len(valid_queue)
        
    def run_classification(self, classifier) -> tuple[int, int]:
        logging.info("Starting Classification Phase")
        # In a real app we'd read unclassified emails from buyers.csv
        # Here we just read unique from buyers.csv and classify them
        import csv
        from app.logging.activity_logger import BUYERS_FILE
        
        unique_emails = set()
        try:
            with open(BUYERS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get("email")
                    if email:
                        unique_emails.add(email)
        except FileNotFoundError:
            pass
            
        business, individual = classifier.classify_emails(list(unique_emails))
        append_classified_emails(business, individual)
        
        return len(business), len(individual)
