from exceptions.business_exception import BusinessException
from models.comment import CommentCreate
from models.comment_classification import CommentClassificationCreate
from models.enums.post_status import PostStatus
from models.lead import LeadCreate
from repositories.comment_classification_repository import CommentClassificationRepository
from repositories.comment_repository import CommentRepository
from repositories.lead_repository import LeadRepository
from repositories.post_repository import PostRepository
from services.comments.comment_validator import CommentValidator
from utils.date_utils import parse_unix_timestamp_to_date


class CommentProcessor:
    def __init__(
        self,
        post_repository: PostRepository,
        comment_repository: CommentRepository,
        comment_validator: CommentValidator,
        comment_classification_repository: CommentClassificationRepository,
        lead_repository: LeadRepository,
    ):
        self.post_repository = post_repository
        self.comment_repository = comment_repository
        self.comment_validator = comment_validator
        self.comment_classification_repository = comment_classification_repository
        self.lead_repository = lead_repository

    def get_processable_post(self, media_id):
        post = self.post_repository.find_by_external_id(str(media_id))

        if not post:
            raise BusinessException(f"Post not found for media_id={media_id}")

        self.comment_validator.validate_post_status(post)

        return self.post_repository.update_status(post.id, PostStatus.SCRAPING)

    def iter_comments_from_pages(self, comment_pages):
        for page in comment_pages:
            for raw_comment in page.get("comments", []):
                yield raw_comment

    def create_comment(self, raw_comment, post_id, status=None):
        comment_to_create = self._build_comment_to_create(
            raw_comment,
            post_id,
            status=status,
        )

        return self.comment_repository.create(comment_to_create)

    def _build_comment_to_create(self, raw_comment, post_id, status=None):
        comment_data = {
            "post_id": post_id,
            "external_id": str(raw_comment["media_id"]),
            "author_username": raw_comment["user"]["username"],
            "content": raw_comment["text"],
        }

        created_at = raw_comment.get("created_at")

        if created_at:
            comment_data["published_at"] = parse_unix_timestamp_to_date(created_at)

        if status is not None:
            comment_data["status"] = status

        return CommentCreate(**comment_data)

    def save_classification(self, comment_id, validation):
        classification_to_create = CommentClassificationCreate(
            comment_id=comment_id,
            model=validation.model,
            is_lead=validation.is_lead,
            reason=validation.reason,
        )

        return self.comment_classification_repository.create(classification_to_create)

    def save_lead(self, comment_id, validation):
        if not validation.is_lead or not validation.lead:
            return None

        return self.lead_repository.create(
            LeadCreate(
                comment_id=comment_id,
                **validation.lead,
            )
        )
