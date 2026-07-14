from scrapers.apify_client import ApifyProvider
from scrapers.platforms.tiktok_scraper import TikTokScraper

provider = ApifyProvider()
scraper = TikTokScraper(provider)

results = scraper.search(
    keyword="fitness",
    max_results=10,
)

print(f"\nFound {len(results)} creators\n")

for creator in results:
    print("=" * 60)
    print("Name:", creator.display_name)
    print("Username:", creator.username)
    print("Followers:", creator.followers)
    print("Following:", creator.following)
    print("Posts:", creator.posts)
    print("Verified:", creator.verified)
    print("Profile:", creator.profile_url)
