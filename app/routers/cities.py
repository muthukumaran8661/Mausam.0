"""Saved cities and geocoding API router."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.geocoding import search_cities

router = APIRouter(tags=["Cities & Geocoding"])


@router.get("/api/users/{user_id}/cities", response_model=List[schemas.SavedCityResponse])
def get_user_saved_cities(user_id: int, db: Session = Depends(get_db)):
    """Fetch all saved cities for a user ordered by display order."""
    cities = (
        db.query(models.SavedCity)
        .filter(models.SavedCity.user_id == user_id)
        .order_by(models.SavedCity.display_order.asc(), models.SavedCity.id.asc())
        .all()
    )
    return cities


@router.post("/api/users/{user_id}/cities", response_model=schemas.SavedCityResponse, status_code=status.HTTP_201_CREATED)
def add_saved_city(
    user_id: int,
    city_in: schemas.SavedCityCreate,
    db: Session = Depends(get_db),
):
    """Add a new city to user's saved cities list."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

    # Check for duplicate coordinates or name
    existing = (
        db.query(models.SavedCity)
        .filter(
            models.SavedCity.user_id == user_id,
            models.SavedCity.name == city_in.name,
        )
        .first()
    )
    if existing:
        return existing

    # Determine highest display_order
    max_order = (
        db.query(models.SavedCity.display_order)
        .filter(models.SavedCity.user_id == user_id)
        .order_by(models.SavedCity.display_order.desc())
        .first()
    )
    next_order = (max_order[0] + 1) if max_order else 0

    new_city = models.SavedCity(
        user_id=user_id,
        name=city_in.name,
        state=city_in.state,
        country=city_in.country,
        lat=city_in.lat,
        lon=city_in.lon,
        is_favorite=city_in.is_favorite,
        display_order=next_order,
    )
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@router.delete("/api/users/{user_id}/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_city(
    user_id: int,
    city_id: int,
    db: Session = Depends(get_db),
):
    """Remove a saved city for a user."""
    city = (
        db.query(models.SavedCity)
        .filter(models.SavedCity.id == city_id, models.SavedCity.user_id == user_id)
        .first()
    )
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved city not found")

    db.delete(city)
    db.commit()
    return None


@router.get("/api/geocode", response_model=List[schemas.GeocodeCity])
async def geocode_query(
    q: str = Query(..., min_length=2, description="City name to search")
):
    """Geocode autocomplete search for locations."""
    return await search_cities(q)
