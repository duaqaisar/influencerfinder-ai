import os
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables from a .env file into the process environment
load_dotenv()

class ApifyProvider:
    """
    Handles communication with the Apify API.
    """

    def __init__(self):
        # Fetch the Apify API token from environment variables
        token = os.getenv("APIFY_API_TOKEN")
        if not token:
            # Fail fast if the token isn't set, since nothing will work without it
            raise ValueError("APIFY_API_TOKEN not found.")
        # Initialize the Apify client with the token
        self.client = ApifyClient(token)

    def run_actor(self, actor_id: str, run_input: dict):
        """
        Run an Apify actor and return dataset items.
        """
        # Trigger the actor run on Apify and wait for it to complete
        run = self.client.actor(actor_id).call(
            run_input=run_input
        )
        # New Apify client returns an object
        # Get the ID of the dataset containing the actor's output
        dataset_id = run.default_dataset_id
        # Fetch all items from the resulting dataset into a list
        items = list(
            self.client.dataset(dataset_id).iterate_items()
        )
        return items
