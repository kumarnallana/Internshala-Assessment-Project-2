from typing import List
from app.search.base import SearchAdapter
from app.search.live_scraper import search_live_web
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class LinkedInSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("LinkedIn B2B")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        if not self.use_mock:
            try:
                logging.info(f"Executing LIVE LinkedIn Search for: '{keyword}'")
                live_results = search_live_web(f"site:linkedin.com {keyword} procurement buyer email", platform="LinkedIn B2B", max_results=max_results)
                if live_results:
                    return live_results
            except Exception as e:
                logging.warning(f"Live LinkedIn search failed ({e}). Falling back to fixtures.")
                
        return self.mock.search(keyword, max_results)
