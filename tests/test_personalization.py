"""Unit tests for the personalization rule engine."""

import pytest
from app.schemas import (
    CurrentWeather,
    HourlyForecastItem,
    DailyForecastItem,
    KeyMetrics,
    UserPreferenceBase,
)
from app.services.personalization import (
    personalize_insights,
    evaluate_commute_insights,
    evaluate_farming_insights,
    evaluate_fitness_insights,
    evaluate_sensitivities_insights,
    generate_generic_fallback_insights,
)


@pytest.fixture
def mock_weather_data():
    current = CurrentWeather(
        temp=28.0,
        feels_like=31.0,
        temp_min=22.0,
        temp_max=33.0,
        humidity=65,
        wind_speed=11.0,
        wind_direction=90,
        wind_direction_cardinal="E",
        weather_code=1,
        condition_text="Mainly Clear",
        condition_icon="cloud-sun",
        uv_index=7.5,
        aqi=85,
        aqi_label="Moderate",
        aqi_color="#F59E0B",
        visibility_km=10.0,
        pressure_hpa=1012.0,
        sunrise="06:05",
        sunset="18:30",
        is_day=True,
    )

    hourly = [
        HourlyForecastItem(
            time=f"2026-09-30T{h:02d}:00",
            hour_display="Now" if h == 14 else f"{h:02d}:00",
            temp=28.0 + (h % 3),
            precipitation_prob=65 if h in (18, 19) else 10,
            weather_code=61 if h in (18, 19) else 1,
            condition_icon="cloud-rain" if h in (18, 19) else "cloud-sun",
            condition_text="Showers" if h in (18, 19) else "Mainly Clear",
        )
        for h in range(24)
    ]

    daily = [
        DailyForecastItem(
            date=f"2026-09-{30+i:02d}",
            day_display="Today" if i == 0 else ["Thu", "Fri", "Sat", "Sun", "Mon", "Tue"][i-1],
            temp_min=22.0,
            temp_max=33.0,
            precipitation_prob=60 if i == 0 else 20,
            weather_code=1,
            condition_icon="cloud-sun",
            condition_text="Mainly Clear",
        )
        for i in range(7)
    ]

    metrics = KeyMetrics(
        humidity=65,
        wind_speed=11.0,
        wind_direction_cardinal="E",
        uv_index=7.5,
        uv_level="High",
        aqi=85,
        aqi_level="Moderate",
        aqi_color="#F59E0B",
        visibility_km=10.0,
        pressure_hpa=1012.0,
        sunrise="06:05",
        sunset="18:30",
    )

    return current, hourly, daily, metrics


def test_commute_rain_alert(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(
        interests=["commute"],
        commute_evening="18:00",
        commute_morning="08:30"
    )

    insights = evaluate_commute_insights(prefs, hourly, "metric")
    assert len(insights) >= 1
    evening_alert = next((i for i in insights if "Evening Commute" in i.title), None)
    assert evening_alert is not None
    assert evening_alert.severity in ("warning", "caution")
    assert evening_alert.icon == "umbrella"
    assert "65%" in evening_alert.message


def test_farming_spraying_window(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(interests=["farming"])

    # Make sure wind is calm and no rain
    calm_current = current.model_copy(update={"wind_speed": 8.0})
    dry_hourly = [h.model_copy(update={"precipitation_prob": 5}) for h in hourly]

    insights = evaluate_farming_insights(prefs, calm_current, dry_hourly, daily, "metric")
    spray_insight = next((i for i in insights if "Spraying" in i.title), None)
    assert spray_insight is not None
    assert spray_insight.category == "farming"
    assert spray_insight.icon == "leaf"


def test_farming_frost_alert(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(interests=["farming"])

    # Cold overnight low
    cold_daily = [daily[0].model_copy(update={"temp_min": 2.0})] + daily[1:]

    insights = evaluate_farming_insights(prefs, current, hourly, cold_daily, "metric")
    frost_insight = next((i for i in insights if "Frost" in i.title), None)
    assert frost_insight is not None
    assert frost_insight.severity == "warning"
    assert frost_insight.relevance_score >= 95


def test_fitness_optimal_window(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(interests=["fitness"])

    # Ensure good AQI and pleasant morning slot
    pleasant_hourly = list(hourly)
    pleasant_hourly[6] = pleasant_hourly[6].model_copy(update={"temp": 21.0, "precipitation_prob": 0})

    insights = evaluate_fitness_insights(prefs, current, pleasant_hourly, metrics, "metric")
    run_insight = next((i for i in insights if "Running" in i.title or "Workout" in i.title), None)
    assert run_insight is not None
    assert run_insight.category == "fitness"


def test_fitness_poor_aqi_alert(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(interests=["fitness"])

    smog_metrics = metrics.model_copy(update={"aqi": 210, "aqi_level": "Very Unhealthy"})
    insights = evaluate_fitness_insights(prefs, current, hourly, smog_metrics, "metric")
    alert = next((i for i in insights if "Advisory" in i.title or "Air Quality" in i.title), None)
    assert alert is not None
    assert alert.severity == "warning"
    assert "indoors" in alert.message


def test_sensitivities_heat_and_allergies(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(
        sensitivities=["heat", "allergies"]
    )

    hot_current = current.model_copy(update={"feels_like": 39.0, "temp": 37.0})
    dusty_metrics = metrics.model_copy(update={"aqi": 145, "aqi_level": "Unhealthy for Sensitive Groups"})

    insights = evaluate_sensitivities_insights(prefs, hot_current, hourly, dusty_metrics, "metric")
    titles = [i.title for i in insights]
    assert any("Heat" in t for t in titles)
    assert any("Allergy" in t or "Air Quality" in t for t in titles)


def test_generic_fallback_for_anonymous_user(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    top_3, all_insights = personalize_insights(None, current, hourly, daily, metrics, "metric")

    assert len(top_3) <= 3
    assert len(all_insights) >= 2
    # Verify sorted by relevance score
    scores = [i.relevance_score for i in all_insights]
    assert scores == sorted(scores, reverse=True)


def test_personalized_top3_limit(mock_weather_data):
    current, hourly, daily, metrics = mock_weather_data
    prefs = UserPreferenceBase(
        interests=["commute", "fitness", "farming", "travel"],
        sensitivities=["heat", "allergies", "rain"]
    )
    hot_current = current.model_copy(update={"feels_like": 38.0})

    top_3, all_insights = personalize_insights(prefs, hot_current, hourly, daily, metrics, "metric")
    assert len(top_3) == 3
    assert len(all_insights) > 3
    assert top_3[0].relevance_score >= top_3[1].relevance_score >= top_3[2].relevance_score
