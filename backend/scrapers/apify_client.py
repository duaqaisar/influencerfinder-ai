import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()


class ApifyProvider:
    """
    Handles communication with the Apify API.
    """

    def __init__(self):
        token = os.getenv("APIFY_API_TOKEN")

        if not token:
            raise ValueError("APIFY_API_TOKEN not found.")

        self.client = ApifyClient(token)

    def run_actor(self, actor_id: str, run_input: dict):
        """
        Run an Apify actor and return dataset items.
        """

        run = self.client.actor(actor_id).call(
            run_input=run_input
        )

        # New Apify client returns an object
        dataset_id = run.default_dataset_id

        items = list(
            self.client.dataset(dataset_id).iterate_items()
        )

        return items
