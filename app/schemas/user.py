from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: UserRole

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
