from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_employer, get_current_user
from app.db.models import Job as JobModel
from app.db.models import User
from app.db.session import get_db
from app.schemas.job import Job, JobCreate, JobUpdate

router = APIRouter()


@router.post("/", response_model=Job)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employer),
):
    db_job = JobModel(**job.model_dump(), posted_by=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=List[Job])
def list_jobs(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(JobModel)
    if title:
        query = query.filter(JobModel.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(JobModel.category == category)
    if location:
        query = query.filter(JobModel.location.ilike(f"%{location}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/my-jobs", response_model=list[Job])
def get_my_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    my_jobs = db.query(JobModel).filter(
        JobModel.posted_by == current_user.id
    )
    if my_jobs is None:
        raise HTTPException(
            status_code=404, detail="No job posted by current user"
        )
    return my_jobs


@router.get("/{job_id}", response_model=Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=Job)
def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employer),
):
    db_job = (
        db.query(JobModel)
        .filter(
            JobModel.id == job_id,
            JobModel.posted_by == current_user.id,
        )
        .first()
    )
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in job_update.model_dump().items():
        setattr(db_job, key, value)

    db.commit()
    db.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employer),
):
    db_job = (
        db.query(JobModel)
        .filter(
            JobModel.id == job_id,
            JobModel.posted_by == current_user.id,
        )
        .first()
    )
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted"}
