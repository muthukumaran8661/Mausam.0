"""Homepage rendering and aggregated home API router."""

import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.services.weather_provider import OpenMeteoWeatherProvider
from app.services.personalization import personalize_insights
from app.services.cache import (
    generate_cache_key,
    get_cached_weather,
    set_cached_weather,
    get_stale_weather,
)
from app.routers.alerts import get_weather_alerts

router = APIRouter(tags=["Home"])
templates = Jinja2Templates(directory="app/templates")
weather_provider = OpenMeteoWeatherProvider()


@router.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    """Render the mobile-first Mausam homepage template."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_title": "Mausam - Personalized Weather"},
    )


@router.get("/api/home", response_model=schemas.HomeApiResponse)
async def get_home_data(
    user_id: Optional[int] = Query(None, description="User ID"),
    lat: Optional[float] = Query(None, ge=-90.0, le=90.0, description="Latitude"),
    lon: Optional[float] = Query(None, ge=-180.0, le=180.0, description="Longitude"),
    city_name: Optional[str] = Query(None, description="Location name"),
    db: Session = Depends(get_db),
):
    """Aggregated homepage data combining live/cached weather, personalization, alerts, and saved cities."""
    # 1. Retrieve User and Preferences
    user_obj = None
    pref_schema = None
    user_saved_cities_db: List[models.SavedCity] = []
    location_name = city_name or "New Delhi"
    target_lat = lat
    target_lon = lon

    if user_id:
        user_obj = db.query(models.User).filter(models.User.id == user_id).first()
        if user_obj:
            user_saved_cities_db = user_obj.saved_cities
            if user_obj.preference:
                pref_schema = schemas.UserPreferenceBase(
                    units=user_obj.preference.units,
                    language=user_obj.preference.language,
                    interests=user_obj.preference.interests or ["commute", "fitness"],
                    sensitivities=user_obj.preference.sensitivities or [],
                    commute_morning=user_obj.preference.commute_morning or "08:30",
                    commute_evening=user_obj.preference.commute_evening or "18:00",
                )

    # If coordinates not supplied, pick from favorite/first saved city or default
    if target_lat is None or target_lon is None:
        if user_saved_cities_db:
            fav = next((c for c in user_saved_cities_db if c.is_favorite), user_saved_cities_db[0])
            target_lat, target_lon = fav.lat, fav.lon
            location_name = fav.name
        else:
            target_lat, target_lon = 28.6139, 77.2090
            location_name = "New Delhi"

    units = pref_schema.units if pref_schema else "metric"
    cache_key = generate_cache_key(target_lat, target_lon, units)

    # 2. Fetch Weather (Cache -> Live -> Stale Fallback)
    is_stale = False
    freshness_text = "Live data"
    weather_data = get_cached_weather(cache_key)

    if not weather_data:
        try:
            weather_data = await weather_provider.get_weather(target_lat, target_lon, units)
            set_cached_weather(cache_key, weather_data)
        except Exception:
            # Attempt stale retrieval
            stale_tuple = get_stale_weather(cache_key)
            if stale_tuple:
                weather_data, mins_ago = stale_tuple
                is_stale = True
                freshness_text = f"Updated {mins_ago} min ago"
            else:
                weather_data = weather_provider._generate_fallback_data(target_lat, target_lon, units)
                set_cached_weather(cache_key, weather_data)

    current: schemas.CurrentWeather = weather_data["current"]
    hourly: List[schemas.HourlyForecastItem] = weather_data["hourly"]
    daily: List[schemas.DailyForecastItem] = weather_data["daily"]
    metrics: schemas.KeyMetrics = weather_data["metrics"]

    # 3. Personalize Insights
    top_3_insights, all_ranked_insights = personalize_insights(
        preferences=pref_schema,
        current=current,
        hourly=hourly,
        daily=daily,
        metrics=metrics,
        units=units,
    )

    # 4. Fetch Active Alerts
    alerts = await get_weather_alerts(lat=target_lat, lon=target_lon)

    # 5. Fetch mini-weather for Saved Cities concurrently
    async def fetch_city_mini(sc: models.SavedCity) -> schemas.SavedCityMiniWeather:
        sc_key = generate_cache_key(sc.lat, sc.lon, units)
        sc_weather = get_cached_weather(sc_key)
        if not sc_weather:
            try:
                sc_weather = await weather_provider.get_weather(sc.lat, sc.lon, units)
                set_cached_weather(sc_key, sc_weather)
            except Exception:
                sc_weather = weather_provider._generate_fallback_data(sc.lat, sc.lon, units)
        sc_curr = sc_weather["current"]
        return schemas.SavedCityMiniWeather(
            id=sc.id,
            name=sc.name,
            state=sc.state,
            country=sc.country,
            lat=sc.lat,
            lon=sc.lon,
            temp=sc_curr.temp,
            condition_text=sc_curr.condition_text,
            condition_icon=sc_curr.condition_icon,
            temp_min=sc_curr.temp_min,
            temp_max=sc_curr.temp_max,
            is_favorite=sc.is_favorite,
        )

    saved_cities_mini: List[schemas.SavedCityMiniWeather] = []
    if user_saved_cities_db:
        import asyncio
        tasks = [fetch_city_mini(sc) for sc in user_saved_cities_db]
        saved_cities_mini = await asyncio.gather(*tasks)

    # 6. Assemble Home Response
    user_response = None
    if user_obj:
        user_response = schemas.UserResponse(
            id=user_obj.id,
            name=user_obj.name,
            email=user_obj.email,
            created_at=user_obj.created_at,
            preference=schemas.UserPreferenceResponse.model_validate(user_obj.preference) if user_obj.preference else None,
            saved_cities=[schemas.SavedCityResponse.model_validate(c) for c in user_saved_cities_db],
        )

    active_interests = pref_schema.interests if pref_schema else ["commute", "fitness"]

    return schemas.HomeApiResponse(
        user=user_response,
        location_name=location_name,
        lat=target_lat,
        lon=target_lon,
        units=units,
        current=current,
        hourly=hourly,
        daily=daily,
        metrics=metrics,
        insights_top=top_3_insights,
        insights_all=all_ranked_insights,
        alerts=alerts,
        saved_cities=saved_cities_mini,
        active_interests=active_interests,
        is_stale=is_stale,
        freshness_text=freshness_text,
        updated_at=datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M UTC"),
    )
