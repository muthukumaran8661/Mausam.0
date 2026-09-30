"""Unit tests for the caching layer and stale fallback."""

import time
from app.services.cache import (
    generate_cache_key,
    get_cached_weather,
    set_cached_weather,
    get_stale_weather,
    clear_all_caches,
)


def test_cache_set_and_get():
    clear_all_caches()
    key = generate_cache_key(28.6139, 77.2090, "metric")
    fake_data = {"location": "Delhi", "temp": 28.5}

    # Before setting, should be None
    assert get_cached_weather(key) is None

    # After setting, should return the cached object
    set_cached_weather(key, fake_data)
    cached = get_cached_weather(key)
    assert cached is not None
    assert cached["temp"] == 28.5


def test_stale_fallback_retrieval():
    clear_all_caches()
    key = generate_cache_key(19.0760, 72.8777, "metric")
    fake_data = {"location": "Mumbai", "temp": 31.0}

    set_cached_weather(key, fake_data)

    # Directly retrieve stale weather
    stale_result = get_stale_weather(key)
    assert stale_result is not None
    data, minutes_ago = stale_result
    assert data["location"] == "Mumbai"
    assert minutes_ago >= 1  # Minimum 1 minute report
