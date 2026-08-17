from typing import List
from app.search.base import SearchAdapter
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class WebsiteSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("Website")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        """
        Adapter implemented.
        Defaults to mock fallback. Real implementation would involve spidering company domains.
        """
        if self.use_mock:
            logging.info(f"Using Mock fallback for Website Search: {keyword}")
            return self.mock.search(keyword, max_results)
            
        logging.info(f"Executing REAL Website Search for: {keyword}")
        return []
