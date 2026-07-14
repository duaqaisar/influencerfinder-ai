from typing import List

from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper


class YouTubeScraper(BaseScraper):
    """
    YouTube scraper using the Apify YouTube Scraper.
    """

    ACTOR_ID = "streamers/youtube-scraper"

    def __init__(self):
        self.provider = ApifyProvider()

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> List[Influencer]:

        run_input = {
            "searchQueries": [query],
            "maxResults": limit,
            "maxResultsShorts": 0,
            "maxResultStreams": 0,
            "downloadSubtitles": False,
            "aiVideoSummary": False,
            "aiVideoDescription": False,
        }

        items = self.provider.run_actor(
            self.ACTOR_ID,
            run_input,
        )

        influencers = []
        seen = set()

        for item in items:

            username = (
                item.get("channelUsername")
                or item.get("channelName")
                or ""
            )

            if not username:
                continue

            if username in seen:
                continue

            seen.add(username)

            display_name = (
                item.get("channelName")
                or username
            )

            bio = (
                item.get("text")
                or item.get("translatedText")
                or ""
            )

            followers = (
                item.get("numberOfSubscribers")
                or 0
            )

            profile_url = (
                item.get("channelUrl")
                or ""
            )

            profile_image = (
                item.get("thumbnailUrl")
                or ""
            )

            influencer = Influencer(
                platform="youtube",
                username=username,
                display_name=display_name,
                bio=bio,
                category=query,
                followers=int(followers),
                following=0,
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
            f"YouTube channel '{username}' not found."
        )
