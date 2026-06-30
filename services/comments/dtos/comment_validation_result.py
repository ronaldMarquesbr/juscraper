from models.enums.comment_status import CommentStatus
from models.lead import LeadCreate


class CommentValidationResult:
    def __init__(
        self,
        status: CommentStatus,
        is_lead: bool,
        reason: str | None = None,
        model: str | None = None,
        lead: LeadCreate | None = None,
    ):
        self.status = status
        self.is_lead = is_lead
        self.reason = reason
        self.model = model
        self.lead = lead
