from scrapers.apify_client import ApifyProvider

# Initialize the Apify provider (sets up the client using the API token)
provider = ApifyProvider()

try:
    # Attempt to fetch metadata for the "tiktok-scraper" actor from Apify
    actor = provider.client.actor("apify/tiktok-scraper").get()
    # Print the actor's details if successfully retrieved
    print(actor)
except Exception as e:
    # If retrieval fails, print the exception type and message for debugging
    print(type(e).__name__)
    print(e)
