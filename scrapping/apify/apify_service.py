import os
from apify_client import ApifyClient


class ApifyService:
    def __init__(self):
        self.client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

    def run_actor(self, actor_identifier, run_input):
        actor_run = self.client.actor(
            actor_identifier
        ).call(run_input=run_input)

        dataset_id = actor_run["defaultDatasetId"]
        dataset = self.client.dataset(dataset_id)

        return list(dataset.iterate_items())
