from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    post_id: int
    external_id: str
    author_username: str
    content: str
    published_at: date | None = None
    status: str | None = None
    updated_at: datetime | None = None


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    post_id: int
    external_id: str
    author_username: str
    content: str
    published_at: date | None = None
    status: str | None = None
