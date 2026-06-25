from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    platform: str
    external_id: str
    url: str
    published_at: date | None = None
    status: str | None = None
    updated_at: datetime | None = None
    author_username: str


class PostCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    platform: str
    external_id: str
    url: str
    published_at: date | None = None
    status: str | None = None
    author_username: str
