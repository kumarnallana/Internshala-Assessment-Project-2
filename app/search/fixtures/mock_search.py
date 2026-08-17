from typing import List
from app.search.base import SearchAdapter

class MockSearchAdapter(SearchAdapter):
    def __init__(self, platform_name: str = "MockPlatform"):
        self.platform_name = platform_name

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        # Deterministic sample fixtures
        return [
            {
                "raw_text": f"We sell {keyword}. Contact: business@singingbowls-demo.com",
                "buyer_name": "John Doe",
                "company_name": "Demo Bowls Inc",
                "website": "singingbowls-demo.com",
                "country": "USA",
                "source_platform": self.platform_name
            },
            {
                "raw_text": "Looking to buy. My email is individual.buyer@example.com",
                "buyer_name": "Jane Smith",
                "company_name": "",
                "website": "",
                "country": "UK",
                "source_platform": self.platform_name
            },
            {
                "raw_text": "Invalid placeholder: noreply@example.com",
                "buyer_name": "Placeholder Corp",
                "company_name": "Placeholder Corp",
                "website": "example.com",
                "country": "Canada",
                "source_platform": self.platform_name
            },
            {
                "raw_text": "No email included here.",
                "buyer_name": "No Email LLC",
                "company_name": "No Email LLC",
                "website": "",
                "country": "Australia",
                "source_platform": self.platform_name
            }
        ]
