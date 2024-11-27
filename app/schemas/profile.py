from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None
    skills: list[str] | None = None
    experience: str | None = None
    company_name: str | None = None
    company_description: str | None = None

class Profile(BaseModel):
    id: int
    name: str
    email: str
    role: str
    bio: str | None = None
    skills: list[str] | None = None
    experience: str | None = None
    company_name: str | None = None
    company_description: str | None = None

    class Config:
        from_attributes = True
