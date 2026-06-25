from scrapping.apify.constants.apify_actors_constants import INSTAGRAM_HASHTAG_SCRAPER
from scrapping.apify.apify_service import ApifyService


class ApifyInstagramSearch:
    def __init__(self, apify_service: ApifyService):
        self.apify_service = apify_service

    def get_posts_by_hashtags(
        self, 
        hashtags,
        results_type="posts",
        results_limit=20
    ):
        run_input = {
            "hashtags": hashtags,
            "results_type": results_type,
            "resultsLimit": results_limit
        }

        return self.apify_service.run_actor(
            actor_identifier=INSTAGRAM_HASHTAG_SCRAPER,
            run_input=run_input
        )
