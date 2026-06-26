from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from models.enums.post_status import PostStatus


class Post(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    platform: str
    external_id: str
    url: str
    published_at: date | None = None
    status: PostStatus | None = None
    updated_at: datetime | None = None
    author_username: str


class PostCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    platform: str
    external_id: str
    url: str
    published_at: date | None = None
    status: PostStatus | None = None
    author_username: str
