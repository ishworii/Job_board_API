from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class ApplicationCreate(BaseModel):
    job_id: int
    resume_url: str | None = None

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class Application(BaseModel):
    id: int
    job_id: int
    user_id: int
    resume_url: str | None = None
    status: ApplicationStatus
    applied_at: datetime

    class Config:
        from_attributes = True
