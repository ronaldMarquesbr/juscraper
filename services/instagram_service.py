from scrapping.apify.apify_instagram_search import ApifyInstagramSearch
from scrapping.apify.constants.defaults import DEFAULT_RESULTS_LIMIT
from scrapping.apify.domain.results_type import ResultsType

from repositories.post_repository import PostRepository
from services.posts.reel_processor import ReelProcessor


class InstagramService:
    def __init__(
        self,
        apify_search: ApifyInstagramSearch,
        post_repository: PostRepository,
        reel_processor: ReelProcessor | None = None,
    ) -> None:
        self.apify_search = apify_search
        self.post_repository = post_repository
        self.reel_processor = reel_processor or ReelProcessor(post_repository)

    def process_reels(self, hashtags, results_limit=DEFAULT_RESULTS_LIMIT):
        reels = self.apify_search.get_posts_by_hashtags(
            hashtags,
            ResultsType.REELS,
            results_limit,
        )

        saved_posts = []

        for reel in reels:
            if not self.reel_processor.is_reel_eligible(reel):
                continue

            post_to_create = self.reel_processor.map_reel_to_create_post(reel)
            saved_post = self.post_repository.create(post_to_create)
            saved_posts.append(saved_post)

        return saved_posts