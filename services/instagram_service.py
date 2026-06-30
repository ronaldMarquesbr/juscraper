from scrapping.apify.apify_instagram_search import ApifyInstagramSearch
from scrapping.apify.constants.defaults import DEFAULT_RESULTS_LIMIT
from scrapping.apify.domain.results_type import ResultsType
from scrapping.instagram.instagram_scrapper import InstagramScrapper

from models.enums.post_status import PostStatus
from repositories.post_repository import PostRepository
from services.comments.comment_processor import CommentProcessor
from services.comments.comment_validator import CommentValidator
from services.posts.reel_processor import ReelProcessor


class InstagramService:
    def __init__(
        self,
        apify_search: ApifyInstagramSearch,
        post_repository: PostRepository,
        reel_processor: ReelProcessor,
        instagram_scrapper: InstagramScrapper,
        comment_validator: CommentValidator,
        comment_processor: CommentProcessor,
    ) -> None:
        self.apify_search = apify_search
        self.post_repository = post_repository
        self.reel_processor = reel_processor
        self.instagram_scrapper = instagram_scrapper
        self.comment_validator = comment_validator
        self.comment_processor = comment_processor

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

    def process_post_comments(self, media_id):
        post = self.comment_processor.get_processable_post(media_id)

        try:
            comment_pages = self.instagram_scrapper.get_comments(media_id)
            saved_comments = []

            for raw_comment in self.comment_processor.iter_comments_from_pages(
                comment_pages
            ):
                if self.comment_validator.is_already_processed(raw_comment):
                    continue

                validation = self.comment_validator.classify(raw_comment)

                saved_comment = self.comment_processor.create_comment(
                    raw_comment,
                    post.id,
                    status=validation.status,
                )
                saved_comments.append(saved_comment)

                self.comment_processor.save_classification(
                    saved_comment.id,
                    validation,
                )
                self.comment_processor.save_lead(saved_comment.id, validation)

            self.post_repository.update_status(post.id, PostStatus.COMPLETED)

            return saved_comments
        except Exception:
            self.post_repository.update_status(post.id, PostStatus.FAILED)
            raise
