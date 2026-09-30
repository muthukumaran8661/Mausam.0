"""Severe weather alerts API router."""

import datetime
from typing import List
from fastapi import APIRouter, Query
from app.schemas import AlertItem
from app.services.weather_provider import OpenMeteoWeatherProvider
from app.services.cache import generate_cache_key, get_cached_weather

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
weather_provider = OpenMeteoWeatherProvider()


@router.get("", response_model=List[AlertItem])
async def get_weather_alerts(
    lat: float = Query(28.6139, ge=-90.0, le=90.0),
    lon: float = Query(77.2090, ge=-180.0, le=180.0),
):
    """Retrieve active meteorological and air quality alerts for given coordinates."""
    # Check cache first
    cache_key = generate_cache_key(lat, lon, "metric")
    weather = get_cached_weather(cache_key)
    if not weather:
        weather = await weather_provider.get_weather(lat, lon, "metric")

    alerts: List[AlertItem] = []
    curr = weather["current"]
    metrics = weather["metrics"]
    daily = weather.get("daily", [])

    now = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime("%Y-%m-%d %H:%M UTC")
    exp_str = (now + datetime.timedelta(hours=12)).strftime("%Y-%m-%d %H:%M UTC")

    # 1. Severe Heat Advisory
    if curr.feels_like >= 40.0:
        alerts.append(
            AlertItem(
                id=f"heat-warn-{int(lat)}-{int(lon)}",
                title="Extreme Heat Warning",
                severity="extreme",
                severity_color="red",
                description=f"Dangerous heat index ({curr.feels_like}°C). Risk of heat exhaustion or heat stroke during prolonged outdoor activity.",
                effective=now_str,
                expires=exp_str,
                source="National Meteorological Department",
            )
        )
    elif curr.feels_like >= 36.0:
        alerts.append(
            AlertItem(
                id=f"heat-adv-{int(lat)}-{int(lon)}",
                title="Heat Advisory in Effect",
                severity="warning",
                severity_color="amber",
                description=f"High temperature and humidity causing elevated apparent temperature of {curr.feels_like}°C. Take precautions if outdoors.",
                effective=now_str,
                expires=exp_str,
                source="National Meteorological Department",
            )
        )

    # 2. Thunderstorm / Severe Rain Alert
    if curr.weather_code in (95, 96, 99):
        alerts.append(
            AlertItem(
                id=f"tstorm-{int(lat)}-{int(lon)}",
                title="Severe Thunderstorm Alert",
                severity="extreme",
                severity_color="red",
                description="Active thunderstorm with lightning and gusty winds observed in the vicinity. Seek sturdy shelter immediately.",
                effective=now_str,
                expires=exp_str,
                source="Severe Weather Warning Center",
            )
        )
    elif curr.weather_code in (65, 82):
        alerts.append(
            AlertItem(
                id=f"heavy-rain-{int(lat)}-{int(lon)}",
                title="Heavy Rainfall Warning",
                severity="warning",
                severity_color="amber",
                description="Intense localized downpours causing reduced roadway visibility and localized waterlogging risk.",
                effective=now_str,
                expires=exp_str,
                source="Regional Hydrological Service",
            )
        )

    # 3. Hazardous Air Quality Alert
    if metrics.aqi > 200:
        alerts.append(
            AlertItem(
                id=f"aqi-severe-{int(lat)}-{int(lon)}",
                title="Severe Air Quality Alert (AQI > 200)",
                severity="extreme",
                severity_color="red",
                description=f"Air Quality Index has reached hazardous level ({metrics.aqi}). Wear N95 masks and run indoor air purifiers.",
                effective=now_str,
                expires=exp_str,
                source="Central Pollution Control Board",
            )
        )
    elif metrics.aqi > 150:
        alerts.append(
            AlertItem(
                id=f"aqi-warn-{int(lat)}-{int(lon)}",
                title="Air Quality Advisory (AQI 151-200)",
                severity="warning",
                severity_color="amber",
                description=f"Unhealthy air conditions (AQI {metrics.aqi}). Children and elderly individuals should avoid outdoor physical exertion.",
                effective=now_str,
                expires=exp_str,
                source="Central Pollution Control Board",
            )
        )

    # 4. Dense Fog Alert
    if curr.weather_code in (45, 48) or curr.visibility_km < 1.0:
        alerts.append(
            AlertItem(
                id=f"fog-{int(lat)}-{int(lon)}",
                title="Dense Fog Advisory",
                severity="watch",
                severity_color="yellow",
                description="Visibility restricted under 1,000 meters. Commuters should use fog lights and maintain safe braking distances.",
                effective=now_str,
                expires=exp_str,
                source="Highway Weather Patrol",
            )
        )

    # Demo default advisory if no severe alerts are active so the UI always has realistic capability to display alerts
    if not alerts:
        alerts.append(
            AlertItem(
                id=f"uv-advisory-{int(lat)}-{int(lon)}",
                title="UV & Sun Exposure Advisory",
                severity="watch",
                severity_color="yellow",
                description=f"Peak afternoon UV Index at {metrics.uv_index} ({metrics.uv_level}). Sun protection recommended between 11:30 AM and 3:30 PM.",
                effective=now_str,
                expires=exp_str,
                source="Atmospheric Health Watch",
            )
        )

    return alerts
