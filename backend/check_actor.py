from scrapers.apify_client import ApifyProvider

provider = ApifyProvider()

try:
    actor = provider.client.actor("apify/tiktok-scraper").get()
    print(actor)
except Exception as e:
    print(type(e).__name__)
    print(e)
