from typing import List
from app.search.base import SearchAdapter
from app.search.fixtures.mock_search import MockSearchAdapter
import logging

class DirectorySearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("Directory")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        """
        Adapter implemented.
        Defaults to mock fallback to ensure safe demonstration without hitting live directories.
        """
        if self.use_mock:
            logging.info(f"Using Mock fallback for Directory Search: {keyword}")
            return self.mock.search(keyword, max_results)
            
        logging.info(f"Executing REAL Directory Search for: {keyword}")
        return []
