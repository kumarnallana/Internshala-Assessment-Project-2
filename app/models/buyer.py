from dataclasses import dataclass
from typing import Optional

@dataclass
class BuyerRecord:
    email: str
    buyer_name: Optional[str] = None
    company_name: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    source_platform: Optional[str] = None

    def to_dict(self):
        return {
            "email": self.email,
            "buyer_name": self.buyer_name or "",
            "company_name": self.company_name or "",
            "website": self.website or "",
            "country": self.country or "",
            "source_platform": self.source_platform or ""
        }
