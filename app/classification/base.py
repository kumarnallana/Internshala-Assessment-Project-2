from abc import ABC, abstractmethod
from typing import List, Tuple

class BaseClassifier(ABC):
    @abstractmethod
    def classify_emails(self, emails: List[str]) -> Tuple[List[str], List[str]]:
        """
        Takes a list of unique emails and returns a tuple:
        (business_emails, individual_emails)
        """
        pass
