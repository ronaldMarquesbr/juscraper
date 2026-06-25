from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Lead(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    name: str | None = None
    username: str | None = None
    problem_description: str
    category: str
    status: str | None = None
    updated_at: datetime | None = None
    comment_id: int | None = None


class LeadCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    name: str | None = None
    username: str | None = None
    problem_description: str
    category: str
    status: str | None = None
    comment_id: int | None = None
