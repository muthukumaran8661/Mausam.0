"""User and user preferences API router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/{user_id}/preferences", response_model=schemas.UserPreferenceResponse)
def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    """Fetch user settings, units, interests, and sensitivities."""
    pref = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if not pref:
        # Check if user exists
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        # Create default preference if missing
        pref = models.UserPreference(user_id=user_id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("/{user_id}/preferences", response_model=schemas.UserPreferenceResponse)
def update_user_preferences(
    user_id: int,
    pref_update: schemas.UserPreferenceUpdate,
    db: Session = Depends(get_db),
):
    """Update user preferences (units, language, interests, sensitivities, commute times)."""
    pref = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if not pref:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        pref = models.UserPreference(user_id=user_id)
        db.add(pref)

    update_data = pref_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pref, key, value)

    db.commit()
    db.refresh(pref)
    return pref


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Fetch full user profile with preferences and saved cities."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    return user
