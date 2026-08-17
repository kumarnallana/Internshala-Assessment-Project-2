from typing import List
from app.search.base import SearchAdapter
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class GoogleSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("Google")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        if self.use_mock:
            logging.info(f"Using Mock for Google Search: {keyword}")
            return self.mock.search(keyword, max_results)
            
        # REAL scraping logic would go here
        # E.g. Using BeautifulSoup on Google search results
        # If it fails, log the failure and return gracefully.
        logging.info(f"Executing REAL Google Search for: {keyword}")
        return []
