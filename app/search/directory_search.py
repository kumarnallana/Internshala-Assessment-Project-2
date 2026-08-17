from typing import List
from app.search.base import SearchAdapter
from app.search.live_scraper import search_live_web
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class DirectorySearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = False):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("B2B Directory")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        if not self.use_mock:
            try:
                logging.info(f"Executing LIVE Directory Search for: '{keyword}'")
                live_results = search_live_web(f"{keyword} B2B Trade Directory supplier buyer", platform="B2B Directory", max_results=max_results)
                if live_results:
                    return live_results
            except Exception as e:
                logging.warning(f"Live directory search failed ({e}). Falling back to fixtures.")
                
        return self.mock.search(keyword, max_results)
