from typing import List
from scrapers.apify_client import ApifyProvider
from scrapers.models.influencer import Influencer
from scrapers.platforms.base_scraper import BaseScraper

# Scraper implementation for fetching influencer/page data from Facebook via Apify
class FacebookScraper(BaseScraper):
    # Replace with the exact Actor ID from the Apify page
    # ID of the Apify actor used to scrape Facebook pages
    ACTOR_ID = "Us34x9p7VgjCz99H6"

    def __init__(self):
        # Initialize the Apify provider used to run the scraping actor
        self.provider = ApifyProvider()

    def search(
        self,
        query: str,
        limit: int = 20,
    ) -> List[Influencer]:
        # Build the input payload for the Apify actor run
        run_input = {
            "categories": [query],   # Search category/keyword
            "resultsLimit": limit,   # Max number of results to fetch
        }
        # Run the actor and get the raw scraped items
        items = self.provider.run_actor(
            self.ACTOR_ID,
            run_input,
        )
        
        influencers = []
        for item in items:
            # Extract bio text from either "about_me" or "info" fields, depending on what's available
            bio = ""
            if item.get("about_me"):
                bio = item["about_me"].get("text", "")
            elif item.get("info"):
                bio = " ".join(item["info"])
            
            # Map raw scraped fields into a standardized Influencer object
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
        # Reuse search() with a limit of 1 to fetch a single page's profile
        profiles = self.search(
            username,
            limit=1,
        )
        if profiles:
            return profiles[0]
        # Raise an error if no matching page was found
        raise ValueError(
            f"Facebook page '{username}' not found."
        )
