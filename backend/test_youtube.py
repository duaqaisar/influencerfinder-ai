from scrapers.platforms.youtube_scraper import YouTubeScraper
from pprint import pprint
scraper = YouTubeScraper()

results = scraper.search(
    query="fitness",
    limit=5,
)

print(f"\nFound {len(results)} videos\n")

for item in results:

    print("=" * 60)

    print(item.get("title"))

    print(item.get("channelName"))

    print(item.get("viewCount"))

    print(item.get("channelUrl"))
    print(type(results))
    print()

    pprint(results[0])
