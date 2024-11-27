from fastapi import FastAPI

from app.api import auth
from app.db.models import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Board API")

app.include_router(auth.router, tags=["authentication"], prefix="/api")
