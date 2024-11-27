from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="sqlite:///./job_board.db")
    SECRET_KEY: str = Field(default="1a3ae01d724da710b3ad5f58c597f347b835e8ee395aa0dfa16b839e554bd59f")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    class Config:
        env_file = ".env"

settings = Settings()
