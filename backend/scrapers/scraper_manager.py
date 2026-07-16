from concurrent.futures import ThreadPoolExecutor
from scrapers.platforms.instagram_scraper import InstagramScraper
from scrapers.platforms.tiktok_scraper import TikTokScraper
from scrapers.platforms.youtube_scraper import YouTubeScraper
from scrapers.platforms.facebook_scraper import FacebookScraper

# Manages scraping across multiple social media platforms
class ScraperManager:
    def __init__(self):
        # Map of platform name -> corresponding scraper instance
        self.scrapers = {
            "instagram": InstagramScraper(),
            "tiktok": TikTokScraper(),
            "youtube": YouTubeScraper(),
            "facebook": FacebookScraper(),
        }

    def search_platform(
        self,
        platform,
        query,
        limit=10,
    ):
        # Get the scraper for the requested platform
        scraper = self.scrapers[platform]
        # Run the search on that platform and return results
        return scraper.search(
            query=query,
            limit=limit,
        )

    def search_all(
        self,
        query,
        limit=10,
    ):
        all_results = []
        # Run searches on all platforms concurrently using a thread pool
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            # Submit a search task for each platform
            for platform in self.scrapers:
                futures.append(
                    executor.submit(
                        self.search_platform,
                        platform,
                        query,
                        limit,
                    )
                )
            # Collect results as each task completes
            for future in futures:
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    # Log any errors from individual platform searches without stopping the rest
                    print(e)
        return all_results
