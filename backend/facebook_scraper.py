from typing import List

from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper


class FacebookScraper(BaseScraper):

    # Replace with the exact Actor ID from the Apify page
    ACTOR_ID = "Us34x9p7VgjCz99H6"

    def __init__(self):
        self.provider = ApifyProvider()

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> List[Influencer]:

        run_input = {
            "categories": [query],
            "resultsLimit": limit,
        }

        items = self.provider.run_actor(
            self.ACTOR_ID,
            run_input,
        )

        influencers = []

        for item in items:

            bio = ""

            if item.get("about_me"):
                bio = item["about_me"].get("text", "")

            elif item.get("info"):
                bio = " ".join(item["info"])

            influencer = Influencer(
                platform="Facebook",

                username=item.get("pageName", ""),

                display_name=item.get("title", ""),

                bio=bio,

                followers=item.get("followers", 0),

                verified=False,

                profile_url=item.get("pageUrl", ""),

                profile_image="",
            )

            influencers.append(influencer)

        return influencers

    def get_profile(self, username: str) -> Influencer:

        profiles = self.search(
            username,
            limit=1,
        )

        if profiles:
            return profiles[0]

        raise ValueError(
            f"Facebook page '{username}' not found."
        )
