from scrapers.platforms.instagram_scraper import InstagramScraper

scraper = InstagramScraper()

results = scraper.search(
    "fitness",
    limit=5
)

print(f"\nFound {len(results)} influencers\n")

for influencer in results:

    print("=" * 60)

    print(influencer.username)

    print(influencer.display_name)

    print(influencer.followers)

    print(influencer.profile_url)
