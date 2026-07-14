from typing import List

from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper


class InstagramScraper(BaseScraper):
    """
    Instagram scraper using the official Apify Instagram Scraper.
    """

    ACTOR_ID = "apify/instagram-scraper"

    def __init__(self):
        self.provider = ApifyProvider()

    def search(
        self,
        query: str,
        limit: int = 20
    ) -> List[Influencer]:

        run_input = {
            "search": query,
            "searchType": "user",
            "searchLimit": limit,
            "resultsType": "details"
        }

        items = self.provider.run_actor(
            self.ACTOR_ID,
            run_input
        )

        influencers = []

        for item in items:

            influencer = Influencer(
                platform="Instagram",

                username=item.get("username", ""),

                display_name=item.get(
                    "fullName",
                    ""
                ),

                bio=item.get(
                    "biography",
                    ""
                ),

                followers=item.get(
                    "followersCount",
                    0
                ),

                following=item.get(
                    "followsCount",
                    0
                ),

                posts=item.get(
                    "postsCount",
                    0
                ),

                verified=item.get(
                    "verified",
                    False
                ),

                profile_url=f"https://instagram.com/{item.get('username','')}",

                profile_image=item.get(
                    "profilePicUrl",
                    ""
                ),
            )

            influencers.append(influencer)

        return influencers

    def get_profile(
        self,
        username: str
    ) -> Influencer:

        profiles = self.search(
            username,
            limit=1
        )

        if profiles:
            return profiles[0]

        raise ValueError(
            f"Instagram profile '{username}' not found."
        )
