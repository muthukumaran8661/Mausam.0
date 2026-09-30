"""Pydantic v2 schemas for data validation and API serialization."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# --- Preference Schemas ---
class UserPreferenceBase(BaseModel):
    units: str = Field(default="metric", pattern="^(metric|imperial)$")
    language: str = Field(default="en", pattern="^(en|hi|ta)$")
    interests: List[str] = Field(default_factory=lambda: ["commute", "fitness"])
    sensitivities: List[str] = Field(default_factory=list)
    commute_morning: str = Field(default="08:30", pattern=r"^\d{2}:\d{2}$")
    commute_evening: str = Field(default="18:00", pattern=r"^\d{2}:\d{2}$")


class UserPreferenceUpdate(BaseModel):
    units: Optional[str] = Field(default=None, pattern="^(metric|imperial)$")
    language: Optional[str] = Field(default=None, pattern="^(en|hi|ta)$")
    interests: Optional[List[str]] = None
    sensitivities: Optional[List[str]] = None
    commute_morning: Optional[str] = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    commute_evening: Optional[str] = Field(default=None, pattern=r"^\d{2}:\d{2}$")


class UserPreferenceResponse(UserPreferenceBase):
    id: int
    user_id: int
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --- Saved City Schemas ---
class SavedCityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    state: Optional[str] = Field(default=None, max_length=120)
    country: str = Field(default="India", max_length=100)
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)
    is_favorite: bool = False
    display_order: int = 0


class SavedCityCreate(SavedCityBase):
    pass


class SavedCityResponse(SavedCityBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SavedCityMiniWeather(BaseModel):
    id: int
    name: str
    state: Optional[str] = None
    country: str
    lat: float
    lon: float
    temp: float
    condition_text: str
    condition_icon: str
    temp_min: float
    temp_max: float
    is_favorite: bool = False


# --- User Schemas ---
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    preference: Optional[UserPreferenceResponse] = None
    saved_cities: List[SavedCityResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# --- Weather Metric & Insight Schemas ---
class CurrentWeather(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    wind_speed: float
    wind_direction: int
    wind_direction_cardinal: str
    weather_code: int
    condition_text: str
    condition_icon: str
    uv_index: float
    aqi: int
    aqi_label: str
    aqi_color: str
    visibility_km: float
    pressure_hpa: float
    sunrise: str
    sunset: str
    is_day: bool


class HourlyForecastItem(BaseModel):
    time: str
    hour_display: str
    temp: float
    precipitation_prob: int
    weather_code: int
    condition_icon: str
    condition_text: str


class DailyForecastItem(BaseModel):
    date: str
    day_display: str
    temp_min: float
    temp_max: float
    precipitation_prob: int
    weather_code: int
    condition_icon: str
    condition_text: str


class KeyMetrics(BaseModel):
    humidity: int
    wind_speed: float
    wind_direction_cardinal: str
    uv_index: float
    uv_level: str
    aqi: int
    aqi_level: str
    aqi_color: str
    visibility_km: float
    pressure_hpa: float
    sunrise: str
    sunset: str


class Insight(BaseModel):
    title: str
    message: str
    severity: str  # "info", "advice", "caution", "warning"
    icon: str      # e.g., "umbrella", "running", "leaf", "sun", "wind", "shield-alert"
    relevance_score: int
    category: str  # "commute", "fitness", "farming", "travel", "health", "general"


class AlertItem(BaseModel):
    id: str
    title: str
    severity: str  # "advisory", "watch", "warning", "extreme"
    severity_color: str  # "yellow", "amber", "red"
    description: str
    effective: str
    expires: str
    source: str


class GeocodeCity(BaseModel):
    id: Optional[int] = None
    name: str
    state: Optional[str] = None
    country: str
    lat: float
    lon: float


# --- Aggregated Homepage Response Schema ---
class HomeApiResponse(BaseModel):
    user: Optional[UserResponse] = None
    location_name: str
    lat: float
    lon: float
    units: str
    current: CurrentWeather
    hourly: List[HourlyForecastItem]
    daily: List[DailyForecastItem]
    metrics: KeyMetrics
    insights_top: List[Insight]
    insights_all: List[Insight]
    alerts: List[AlertItem]
    saved_cities: List[SavedCityMiniWeather]
    active_interests: List[str]
    is_stale: bool = False
    freshness_text: str = "Live data"
    updated_at: str
