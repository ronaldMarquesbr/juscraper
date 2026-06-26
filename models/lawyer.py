from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Lawyer(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    name: str
    email: str
    phone_number: str
    specialty: str | None = None
    active: bool | None = None


class LawyerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    name: str
    email: str
    phone_number: str
    specialty: str | None = None
    active: bool | None = None
