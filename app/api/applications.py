from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_employer, get_current_job_seeker, get_current_user
from app.db.models import Application as ApplicationModel
from app.db.models import Job as JobModel
from app.db.models import User
from app.db.session import get_db
from app.schemas.application import Application, ApplicationCreate, ApplicationUpdate

router = APIRouter()

@router.post("/", response_model=Application)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_job_seeker)
):
    job = db.query(JobModel).filter(JobModel.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    existing_application = db.query(ApplicationModel).filter(
        ApplicationModel.job_id == application.job_id,
        ApplicationModel.user_id == current_user.id
    ).first()
    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    db_application = ApplicationModel(
        **application.dict(),
        user_id=current_user.id,
        status="pending"
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/{job_id}", response_model=List[Application])
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employer)
):
    job = db.query(JobModel).filter(
        JobModel.id == job_id,
        JobModel.posted_by == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return db.query(ApplicationModel).filter(ApplicationModel.job_id == job_id).all()

@router.put("/{application_id}", response_model=Application)
def update_application_status(
    application_id: int,
    status_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_employer)
):
    application = db.query(ApplicationModel).join(JobModel).filter(
        ApplicationModel.id == application_id,
        JobModel.posted_by == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = status_update.status
    db.commit()
    db.refresh(application)
    return application
