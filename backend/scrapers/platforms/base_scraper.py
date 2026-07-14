from abc import ABC, abstractmethod
from typing import List

from scrapers.models.influencer import Influencer


class BaseScraper(ABC):
    """
    Abstract base class for all platform scrapers.
    """

    @abstractmethod
    def search(self, query: str, limit: int = 20) -> List[Influencer]:
        """
        Search influencers by keyword.
        """
        pass

    @abstractmethod
    def get_profile(self, username: str) -> Influencer:
        """
        Fetch a single influencer profile.
        """
        pass
