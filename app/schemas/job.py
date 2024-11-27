from datetime import datetime

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str
    category: str
    location: str

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class Job(JobBase):
    id: int
    posted_by: int
    created_at: datetime

    class Config:
        from_attributes = True
