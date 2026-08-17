from typing import List
from app.search.base import SearchAdapter

class MockSearchAdapter(SearchAdapter):
    def __init__(self, platform_name: str = "MockPlatform"):
        self.platform_name = platform_name

    def search(self, keyword: str, max_results: int = 10) -> List[dict]:
        # Deterministic sample fixtures
        return [
            {
                "raw_text": f"Global Wholesale {keyword} Exporter. Inquiries: sales.business@singingbowls-global.com or info@exportbowls.com",
                "buyer_name": "International Trade Co",
                "company_name": "Global Singing Bowls Ltd",
                "website": "singingbowls-global.com",
                "country": "Germany",
                "source_platform": self.platform_name
            },
            {
                "raw_text": f"Looking for bulk order {keyword}. Please reach out to sasikumarnallana956@gmail.com",
                "buyer_name": "Sasi Kumar",
                "company_name": "Kumar Imports",
                "website": "kumar-imports.com",
                "country": "India",
                "source_platform": self.platform_name
            },
            {
                "raw_text": "Independent buyer looking for authentic bowls: individual.buyer@craftmarkets.org",
                "buyer_name": "Jane Smith",
                "company_name": "",
                "website": "",
                "country": "UK",
                "source_platform": self.platform_name
            },
            {
                "raw_text": "Automated system test: noreply@placeholder.com",
                "buyer_name": "Placeholder Corp",
                "company_name": "Placeholder Corp",
                "website": "placeholder.com",
                "country": "Canada",
                "source_platform": self.platform_name
            }
        ]
