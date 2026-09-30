"""Unit tests for weather provider and parsing functions."""

import pytest
from app.services.weather_provider import (
    OpenMeteoWeatherProvider,
    wmo_code_to_info,
    degrees_to_cardinal,
    evaluate_aqi_us,
    evaluate_uv_index,
)


def test_wmo_code_to_info():
    text, icon = wmo_code_to_info(0, is_day=True)
    assert text == "Clear Sky"
    assert icon == "sun"

    text, icon = wmo_code_to_info(0, is_day=False)
    assert icon == "moon"

    text, icon = wmo_code_to_info(61, is_day=True)
    assert "Rain" in text
    assert "rain" in icon

    text, icon = wmo_code_to_info(95, is_day=True)
    assert text == "Thunderstorm"
    assert "lightning" in icon


def test_degrees_to_cardinal():
    assert degrees_to_cardinal(0) == "N"
    assert degrees_to_cardinal(90) == "E"
    assert degrees_to_cardinal(180) == "S"
    assert degrees_to_cardinal(270) == "W"
    assert degrees_to_cardinal(45) == "NE"


def test_evaluate_aqi_us():
    label, color = evaluate_aqi_us(40)
    assert label == "Good"
    assert color == "#10B981"

    label, color = evaluate_aqi_us(85)
    assert label == "Moderate"

    label, color = evaluate_aqi_us(160)
    assert label == "Unhealthy"


def test_evaluate_uv_index():
    assert evaluate_uv_index(2.0) == "Low"
    assert evaluate_uv_index(4.5) == "Moderate"
    assert evaluate_uv_index(7.2) == "High"
    assert evaluate_uv_index(12.0) == "Extreme"


@pytest.mark.asyncio
async def test_fallback_weather_generation():
    provider = OpenMeteoWeatherProvider()
    data = provider._generate_fallback_data(28.6139, 77.2090, "metric")

    assert "current" in data
    assert "hourly" in data
    assert "daily" in data
    assert "metrics" in data

    assert len(data["hourly"]) == 24
    assert len(data["daily"]) == 7
    assert data["current"].temp > 0
