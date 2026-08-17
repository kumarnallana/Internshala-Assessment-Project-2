from typing import List
from app.search.base import SearchAdapter
from app.search.live_scraper import search_live_web
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class GoogleSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("Google Search")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        if not self.use_mock:
            try:
                logging.info(f"Executing LIVE Web Search for: '{keyword}'")
                live_results = search_live_web(keyword, platform="Google Search", max_results=max_results)
                if live_results:
                    return live_results
            except Exception as e:
                logging.warning(f"Live search failed ({e}). Falling back to sample fixtures.")
                
        return self.mock.search(keyword, max_results)
