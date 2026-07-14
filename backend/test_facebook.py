from scrapers.platforms.facebook_scraper import FacebookScraper

scraper = FacebookScraper()

results = scraper.search(
    query="fitness",
    limit=5,
)

print(f"\nFound {len(results)} pages\n")

for page in results:
    print("=" * 60)
    print(page.display_name)
    print(page.username)
    print(page.followers)
    print(page.profile_url)
