from scrapers.apify_client import ApifyProvider
import json

provider = ApifyProvider()

items = provider.run_actor(
    "apify/instagram-scraper",
    {
        "search": "fitness",
        "searchType": "user",
        "searchLimit": 1,
        "resultsType": "details"
    }
)

print(json.dumps(items[0], indent=4))
