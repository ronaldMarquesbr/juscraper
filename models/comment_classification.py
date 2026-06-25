from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentClassification(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    comment_id: int
    model: str | None = None
    is_lead: bool
    reason: str | None = None


class CommentClassificationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    comment_id: int
    model: str | None = None
    is_lead: bool
    reason: str | None = None
