from typing import List

from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper


class FacebookScraper(BaseScraper):
    """
    Facebook scraper using the Apify Facebook Search Scraper.
    """

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
        seen = set()

        for item in items:

            username = item.get("pageName") or ""

            if not username:
                continue

            if username in seen:
                continue

            seen.add(username)

            display_name = (
                item.get("title")
                or username
            )

            bio = (
                item.get("intro")
                or " ".join(item.get("info", []))
                or ""
            )

            followers = int(
                item.get("followers")
                or item.get("likes")
                or 0
            )

            following = int(
                item.get("followings")
                or 0
            )

            profile_url = (
                item.get("pageUrl")
                or item.get("facebookUrl")
                or ""
            )

            profile_image = (
                item.get("profilePictureUrl")
                or ""
            )

            influencer = Influencer(
                platform="facebook",
                username=username,
                display_name=display_name,
                bio=bio,
                category=query,
                followers=followers,
                following=following,
                posts=0,
                engagement_rate=0.0,
                verified=False,
                profile_url=profile_url,
                profile_image=profile_image,
            )

            influencers.append(influencer)

            if len(influencers) >= limit:
                break

        return influencers

    def get_profile(
        self,
        username: str,
    ):

        profiles = self.search(
            username,
            limit=1,
        )

        if profiles:
            return profiles[0]

        raise ValueError(
            f"Facebook page '{username}' not found."
        )
