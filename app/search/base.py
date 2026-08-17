from abc import ABC, abstractmethod
from typing import List

class SearchAdapter(ABC):
    @abstractmethod
    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        """
        Executes a search and returns raw or semi-structured candidate data.
        Returns a list of dicts. Example dict structure:
        {
            "raw_text": "...",
            "buyer_name": "...",
            "company_name": "...",
            "website": "...",
            "country": "...",
            "source_platform": "Google"
        }
        """
        pass
