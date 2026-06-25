from scrapping.apify.constants.actors import INSTAGRAM_HASHTAG_SCRAPER
from scrapping.apify.constants.defaults import DEFAULT_RESULTS_LIMIT
from scrapping.apify.apify_service import ApifyService
from scrapping.apify.domain.results_type import ResultsType


class ApifyInstagramSearch:
    def __init__(self, apify_service: ApifyService):
        self.apify_service = apify_service

    def get_posts_by_hashtags(
        self, 
        hashtags,
        results_type=ResultsType.POSTS,
        results_limit=DEFAULT_RESULTS_LIMIT
    ):
        run_input = {
            "hashtags": hashtags,
            "results_type": results_type.value,
            "resultsLimit": results_limit
        }

        return self.apify_service.run_actor(
            actor_identifier=INSTAGRAM_HASHTAG_SCRAPER,
            run_input=run_input
        )
