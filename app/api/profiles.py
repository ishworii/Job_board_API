from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.profile import Profile, ProfileUpdate

router = APIRouter()

@router.get("/", response_model=Profile)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/", response_model=Profile)
def update_profile(
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user
