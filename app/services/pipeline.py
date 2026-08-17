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
    def __init__(self, keyword: str, use_mock: bool = False):
        self.keyword = keyword or "Singing Bowls"
        self.adapters = [
            GoogleSearchAdapter(use_mock=use_mock),
            FacebookSearchAdapter(use_mock=use_mock),
            LinkedInSearchAdapter(use_mock=use_mock),
            DirectorySearchAdapter(use_mock=use_mock),
            WebsiteSearchAdapter(use_mock=use_mock),
        ]

    def run_discovery(self):
        logging.info(f"Starting Real-time Lead Discovery for keyword: '{self.keyword}'")
        all_buyers = []
        for adapter in self.adapters:
            try:
                results = adapter.search(self.keyword, max_results=6)
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
            except Exception as e:
                logging.warning(f"Error querying adapter {adapter}: {e}")
                
        # Validate and filter
        valid_queue, review_queue = filter_buyers_for_queue(all_buyers)
        
        # Save all discovered leads to buyers.csv
        append_buyers(all_buyers)
        
        logging.info(f"Discovery Complete. Harvested {len(all_buyers)} leads ({len(valid_queue)} valid).")
        return len(all_buyers), len(valid_queue)
        
    def run_classification(self, classifier) -> tuple[int, int, int]:
        logging.info("Starting Classification Phase")
        import csv
        from app.logging.activity_logger import BUYERS_FILE
        
        unique_emails = set()
        try:
            with open(BUYERS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get("email")
                    if email and "@" in email:
                        unique_emails.add(email.strip())
        except FileNotFoundError:
            pass
            
        business, individual, unknown = classifier.classify_emails(list(unique_emails))
        append_classified_emails(business, individual, unknown)
        
        return len(business), len(individual), len(unknown)
