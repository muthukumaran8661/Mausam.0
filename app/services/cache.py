"""In-memory TTL cache with stale-while-revalidate fallback for weather data."""

import time
from typing import Dict, Any, Optional, Tuple
from cachetools import TTLCache
from app.config import get_settings

settings = get_settings()

# Primary TTL Cache (evicts entries after TTL)
_weather_ttl_cache: TTLCache[str, Dict[str, Any]] = TTLCache(
    maxsize=1000,
    ttl=settings.weather_cache_ttl
)

# Persistent in-memory store for stale-while-revalidate fallback (never auto-evicted)
_stale_weather_store: Dict[str, Tuple[Dict[str, Any], float]] = {}


def generate_cache_key(lat: float, lon: float, units: str = "metric") -> str:
    """Generate consistent cache key for coordinates and unit system."""
    return f"{round(lat, 3)}_{round(lon, 3)}_{units.lower()}"


def get_cached_weather(key: str) -> Optional[Dict[str, Any]]:
    """Retrieve weather data from the active TTL cache.

    Returns None if expired or not present.
    """
    return _weather_ttl_cache.get(key)


def set_cached_weather(key: str, data: Dict[str, Any]) -> None:
    """Store fresh weather data in both TTL cache and fallback store."""
    now = time.time()
    _weather_ttl_cache[key] = data
    _stale_weather_store[key] = (data, now)


def get_stale_weather(key: str) -> Optional[Tuple[Dict[str, Any], int]]:
    """Retrieve last known good weather data and minutes since cached.

    Returns:
        (data, minutes_ago) or None if no previous record exists.
    """
    if key in _stale_weather_store:
        data, timestamp = _stale_weather_store[key]
        minutes_ago = max(1, int((time.time() - timestamp) // 60))
        return data, minutes_ago
    return None


def clear_all_caches() -> None:
    """Clear all caches (primarily used in test suites)."""
    _weather_ttl_cache.clear()
    _stale_weather_store.clear()
