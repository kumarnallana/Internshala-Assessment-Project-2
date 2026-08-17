from abc import ABC, abstractmethod
from typing import List

class BaseSender(ABC):
    @abstractmethod
    def send_campaign(self, emails: List[str], subject: str, body: str, attachment_path: str = None) -> tuple[int, int, List[str], List[str], List[str]]:
        """
        Sends emails.
        Returns: (success_count, failed_count, successful_emails, failed_emails, skipped_emails)
        """
        pass
