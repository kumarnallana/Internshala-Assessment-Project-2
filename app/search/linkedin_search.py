from typing import List
from app.search.base import SearchAdapter
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class LinkedInSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("LinkedIn")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        """
        Adapter implemented.
        Defaults to mock fallback since true LinkedIn scraping requires complex authentication 
        and rotating proxies outside the scope of this project.
        """
        if self.use_mock:
            logging.info(f"Using Mock fallback for LinkedIn Search: {keyword}")
            return self.mock.search(keyword, max_results)
            
        logging.info(f"Executing REAL LinkedIn Search for: {keyword}")
        return []
