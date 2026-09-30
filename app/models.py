"""SQLAlchemy ORM models for Users, Preferences, and Saved Cities."""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, default="Guest")
    email = Column(String(255), unique=True, nullable=True, index=True)
    created_at = Column(DateTime, default=utcnow)

    preference = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    saved_cities = relationship("SavedCity", back_populates="user", cascade="all, delete-orphan", order_by="SavedCity.display_order")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    units = Column(String(20), default="metric")  # "metric" (Celsius, km/h) or "imperial" (Fahrenheit, mph)
    language = Column(String(10), default="en")    # "en", "hi", "ta"
    interests = Column(JSON, default=list)        # ["commute", "fitness", "farming", "travel"]
    sensitivities = Column(JSON, default=list)    # ["heat", "cold", "allergies", "rain"]
    commute_morning = Column(String(10), default="08:30")  # e.g. "08:30"
    commute_evening = Column(String(10), default="18:00")  # e.g. "18:00"
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    user = relationship("User", back_populates="preference")


class SavedCity(Base):
    __tablename__ = "saved_cities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    state = Column(String(120), nullable=True)
    country = Column(String(100), nullable=False, default="India")
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    is_favorite = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=utcnow)

    user = relationship("User", back_populates="saved_cities")
