from exceptions.business_exception import BusinessException
from models.enums.post_status import PostStatus
from models.post import Post
from repositories.comment_repository import CommentRepository
from services.comments.dtos.comment_validation_result import CommentValidationResult


class CommentValidator:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def is_already_processed(self, raw_comment):
        external_id = str(raw_comment["pk"])
        return self.comment_repository.exists_by_external_id(external_id)

    def validate_post_status(self, post: Post) -> None:
        if PostStatus.is_processable(post.status):
            return

        post_status = post.status
        status = post_status.value if post_status else None

        raise BusinessException(
            f"Post {post.external_id} cannot be processed (status={status})"
        )

    def classify(self, raw_comment) -> CommentValidationResult:
        # TODO: implementar classificação com IA
        return CommentValidationResult(
            status=None,
            is_lead=False,
            reason=None,
            model=None,
            lead=None,
        )
