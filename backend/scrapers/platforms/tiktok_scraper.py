from typing import List

from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper


class TikTokScraper(BaseScraper):
    """
    TikTok scraper using the Clockworks TikTok Scraper on Apify.
    """

    ACTOR_ID = "clockworks/tiktok-scraper"

    def __init__(self):
        self.provider = ApifyProvider()

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> List[Influencer]:

        actor_input = {
            "searchQueries": [query],
            "searchSection": "/user",
            "profilesPerQuery": limit,
            "resultsPerPage": 5,
        }

        items = self.provider.run_actor(
            self.ACTOR_ID,
            actor_input,
        )

        influencers = []
        seen = set()

        for item in items:

            author = item.get("authorMeta", {})

            username = (
                author.get("name")
                or item.get("author")
                or item.get("uniqueId")
                or ""
            )

            if not username:
                continue

            if username in seen:
                continue

            seen.add(username)

            display_name = (
                author.get("nickName")
                or author.get("nickname")
                or username
            )

            bio = author.get("signature") or ""

            followers = (
                author.get("fans")
                or author.get("fansCount")
                or 0
            )

            following = (
                author.get("following")
                or author.get("followingCount")
                or 0
            )

            posts = (
                author.get("video")
                or author.get("videoCount")
                or 0
            )

            verified = author.get("verified", False)

            profile_image = (
                author.get("avatar")
                or author.get("avatarThumb")
                or ""
            )

            influencer = Influencer(
                platform="tiktok",
                username=username,
                display_name=display_name,
                bio=bio,
                category=query,
                followers=int(followers),
                following=int(following),
                posts=int(posts),
                engagement_rate=0.0,
                verified=verified,
                profile_url=f"https://www.tiktok.com/@{username}",
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
            f"TikTok profile '{username}' not found."
        )
