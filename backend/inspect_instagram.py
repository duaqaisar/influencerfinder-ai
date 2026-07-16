from scrapers.apify_client import ApifyProvider
import json

# Initialize the Apify provider (sets up the client using the API token)
provider = ApifyProvider()

# Run the Instagram scraper actor with a test search
# Searches for a single user matching "fitness" and returns detailed profile info
items = provider.run_actor(
    "apify/instagram-scraper",
    {
        "search": "fitness",       # Search keyword
        "searchType": "user",      # Search for user accounts (not hashtags/locations)
        "searchLimit": 1,          # Only fetch 1 result
        "resultsType": "details"   # Return full profile details rather than just posts
    }
)

# Pretty-print the first result to inspect its structure/fields
print(json.dumps(items[0], indent=4))
