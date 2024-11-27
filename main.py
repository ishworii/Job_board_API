from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import applications, auth, jobs, profiles
from app.db.models import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Board API")

origins = [
    "http://localhost:3000",  
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, tags=["authentication"], prefix="/api")
app.include_router(jobs.router, tags=["jobs"], prefix="/api/jobs")
app.include_router(applications.router, tags=["applications"], prefix="/api/applications")
app.include_router(profiles.router, tags=["profiles"], prefix="/api/profile")
