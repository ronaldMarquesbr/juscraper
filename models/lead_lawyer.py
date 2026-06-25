from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LeadLawyer(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int
    created_at: datetime | None = None
    lead_id: int
    lawyer_id: int
    status: str | None = None


class LeadLawyerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    lead_id: int
    lawyer_id: int
    status: str | None = None
