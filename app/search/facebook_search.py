from typing import List
from app.search.base import SearchAdapter
from app.search.fixtures.mock_search import MockSearchAdapter

class FacebookSearchAdapter(SearchAdapter):
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.mock = MockSearchAdapter("Facebook")

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        if self.use_mock:
            return self.mock.search(keyword, max_results)
        return []
