from concurrent.futures import ThreadPoolExecutor

from scrapers.platforms.instagram_scraper import InstagramScraper
from scrapers.platforms.tiktok_scraper import TikTokScraper
from scrapers.platforms.youtube_scraper import YouTubeScraper
from scrapers.platforms.facebook_scraper import FacebookScraper


class ScraperManager:

    def __init__(self):

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

        scraper = self.scrapers[platform]

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

        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = []

            for platform in self.scrapers:

                futures.append(
                    executor.submit(
                        self.search_platform,
                        platform,
                        query,
                        limit,
                    )
                )

            for future in futures:

                try:
                    results = future.result()
                    all_results.extend(results)

                except Exception as e:
                    print(e)

        return all_results
