"""Personalization rule engine.

Pure functions translating meteorological conditions and user preferences into
ranked, human-centric actionable insights. No network calls.
"""

from typing import List, Optional, Tuple
from app.schemas import (
    CurrentWeather,
    HourlyForecastItem,
    DailyForecastItem,
    KeyMetrics,
    Insight,
    UserPreferenceBase,
)


def _get_commute_hours(time_str: str) -> List[int]:
    """Return hours around a commute time string (e.g. '08:30' -> [8, 9])."""
    try:
        hour = int(time_str.split(":")[0])
        return [hour, (hour + 1) % 24]
    except Exception:
        return [8, 9]


def evaluate_commute_insights(
    preferences: Optional[UserPreferenceBase],
    hourly: List[HourlyForecastItem],
    units: str,
) -> List[Insight]:
    """Evaluate insights for daily commute windows."""
    insights: List[Insight] = []
    if not preferences or "commute" not in preferences.interests:
        return insights

    morning_hours = _get_commute_hours(preferences.commute_morning)
    evening_hours = _get_commute_hours(preferences.commute_evening)

    # Check morning commute
    morning_items = [h for h in hourly if any(f"{hr:02d}:00" in h.time for hr in morning_hours)]
    if morning_items:
        max_rain = max(item.precipitation_prob for item in morning_items)
        if max_rain >= 40:
            insights.append(
                Insight(
                    title="Morning Commute Rain Alert",
                    message=f"Rain probability reaches {max_rain}% around your morning commute ({preferences.commute_morning}). Carry an umbrella.",
                    severity="warning" if max_rain >= 70 else "caution",
                    icon="umbrella",
                    relevance_score=95 if max_rain >= 70 else 85,
                    category="commute",
                )
            )

    # Check evening commute
    evening_items = [h for h in hourly if any(f"{hr:02d}:00" in h.time for hr in evening_hours)]
    if evening_items:
        max_rain_eve = max(item.precipitation_prob for item in evening_items)
        if max_rain_eve >= 40:
            insights.append(
                Insight(
                    title="Evening Commute Showers",
                    message=f"Rain probability rises to {max_rain_eve}% near your evening commute ({preferences.commute_evening}). Keep wet-weather gear ready.",
                    severity="warning" if max_rain_eve >= 70 else "caution",
                    icon="umbrella",
                    relevance_score=96 if max_rain_eve >= 70 else 86,
                    category="commute",
                )
            )
        else:
            # Check pleasant evening commute
            pleasant_eve = all(item.precipitation_prob < 20 for item in evening_items)
            if pleasant_eve and evening_items:
                insights.append(
                    Insight(
                        title="Smooth Evening Commute",
                        message=f"Clear transit expected around {preferences.commute_evening} with no rain in the forecast.",
                        severity="info",
                        icon="compass",
                        relevance_score=60,
                        category="commute",
                    )
                )

    return insights


def evaluate_farming_insights(
    preferences: Optional[UserPreferenceBase],
    current: CurrentWeather,
    hourly: List[HourlyForecastItem],
    daily: List[DailyForecastItem],
    units: str,
) -> List[Insight]:
    """Evaluate insights for agricultural and farming activities."""
    insights: List[Insight] = []
    if not preferences or "farming" not in preferences.interests:
        return insights

    wind_limit = 15.0 if units == "metric" else 10.0
    upcoming_rain_prob = max((h.precipitation_prob for h in hourly[:12]), default=0)

    # Spray window evaluation
    if current.wind_speed <= wind_limit and upcoming_rain_prob < 25:
        insights.append(
            Insight(
                title="Favorable Crop Spraying Window",
                message=f"Gentle breeze ({current.wind_speed} {'km/h' if units == 'metric' else 'mph'}) and low rain risk ({upcoming_rain_prob}%) make today optimal for pesticide or fertilizer spraying.",
                severity="advice",
                icon="leaf",
                relevance_score=90,
                category="farming",
            )
        )
    elif current.wind_speed > wind_limit:
        insights.append(
            Insight(
                title="Spray Drift Caution",
                message=f"Elevated wind speed ({current.wind_speed} {'km/h' if units == 'metric' else 'mph'}) increases spray drift risk. Consider postponing aerial or field spraying.",
                severity="caution",
                icon="wind",
                relevance_score=85,
                category="farming",
            )
        )

    # Irrigation evaluation
    temp_threshold = 32.0 if units == "metric" else 90.0
    rain_next_3_days = sum(d.precipitation_prob > 50 for d in daily[:3])
    if rain_next_3_days >= 2:
        insights.append(
            Insight(
                title="Irrigation: Hold Off",
                message="Substantial rainfall is expected over the next 48-72 hours. Save water and prevent waterlogging by delaying irrigation.",
                severity="advice",
                icon="cloud-rain",
                relevance_score=88,
                category="farming",
            )
        )
    elif current.temp >= temp_threshold and current.humidity <= 45 and upcoming_rain_prob < 20:
        insights.append(
            Insight(
                title="High Soil Evaporation Rate",
                message=f"High temperature ({current.temp}°) and dry air ({current.humidity}%) will rapidly deplete topsoil moisture. Early morning or evening irrigation recommended.",
                severity="advice",
                icon="sun",
                relevance_score=82,
                category="farming",
            )
        )

    # Frost danger
    frost_temp = 3.0 if units == "metric" else 37.0
    if daily and daily[0].temp_min <= frost_temp:
        insights.append(
            Insight(
                title="Ground Frost Risk",
                message=f"Overnight temperature dropping to {daily[0].temp_min}°. Shield sensitive seedlings and cold-vulnerable produce.",
                severity="warning",
                icon="snowflake",
                relevance_score=98,
                category="farming",
            )
        )

    return insights


def evaluate_fitness_insights(
    preferences: Optional[UserPreferenceBase],
    current: CurrentWeather,
    hourly: List[HourlyForecastItem],
    metrics: KeyMetrics,
    units: str,
) -> List[Insight]:
    """Evaluate insights for runners, cyclists, and fitness enthusiasts."""
    insights: List[Insight] = []
    if not preferences or "fitness" not in preferences.interests:
        return insights

    # Check for poor air quality first
    if metrics.aqi > 150:
        insights.append(
            Insight(
                title="Outdoor Workout Advisory",
                message=f"Air Quality Index is {metrics.aqi} ({metrics.aqi_level}). Health guidelines advise moving intense cardio and running indoors today.",
                severity="warning",
                icon="shield-alert",
                relevance_score=94,
                category="fitness",
            )
        )
        return insights

    # Search for an optimal run window in the next 12 hours
    best_slot = None
    min_score = 999
    ideal_low = 16.0 if units == "metric" else 60.0
    ideal_high = 25.0 if units == "metric" else 77.0

    for item in hourly[:12]:
        if item.precipitation_prob <= 20 and ideal_low <= item.temp <= ideal_high:
            score = abs(item.temp - (20.0 if units == "metric" else 68.0)) + item.precipitation_prob
            if score < min_score:
                min_score = score
                best_slot = item

    if best_slot:
        insights.append(
            Insight(
                title="Prime Outdoor Running Window",
                message=f"Great running conditions at {best_slot.hour_display} ({best_slot.temp}°, rain chance {best_slot.precipitation_prob}%). AQI is {metrics.aqi_level}.",
                severity="advice",
                icon="running",
                relevance_score=88,
                category="fitness",
            )
        )
    elif current.temp > (33.0 if units == "metric" else 92.0):
        insights.append(
            Insight(
                title="High Heat Stress on Workouts",
                message=f"Current temperature is {current.temp}°. Schedule exercise during cooler early morning or post-sunset hours, and keep hydration high.",
                severity="caution",
                icon="sun",
                relevance_score=80,
                category="fitness",
            )
        )

    return insights


def evaluate_travel_insights(
    preferences: Optional[UserPreferenceBase],
    daily: List[DailyForecastItem],
    units: str,
) -> List[Insight]:
    """Evaluate insights for travel and weekend getaways."""
    insights: List[Insight] = []
    if not preferences or "travel" not in preferences.interests:
        return insights

    # Look at weekend days
    weekend_items = [d for d in daily if d.day_display in ("Sat", "Sun")]
    if weekend_items:
        rainy_weekend = any(d.precipitation_prob >= 50 for d in weekend_items)
        if rainy_weekend:
            insights.append(
                Insight(
                    title="Weekend Getaway Weather Outlook",
                    message="Scattered rain showers expected this weekend. Factor in extra travel time and pack waterproof jackets.",
                    severity="caution",
                    icon="compass",
                    relevance_score=75,
                    category="travel",
                )
            )
        else:
            avg_max = sum(d.temp_max for d in weekend_items) / len(weekend_items)
            insights.append(
                Insight(
                    title="Pleasant Weekend Travel Ahead",
                    message=f"Sunny and calm conditions forecast for the weekend (avg high {avg_max:.1f}°). Excellent timing for road trips and outdoor sightseeing.",
                    severity="info",
                    icon="compass",
                    relevance_score=72,
                    category="travel",
                )
            )

    return insights


def evaluate_sensitivities_insights(
    preferences: Optional[UserPreferenceBase],
    current: CurrentWeather,
    hourly: List[HourlyForecastItem],
    metrics: KeyMetrics,
    units: str,
) -> List[Insight]:
    """Evaluate health alerts based on user physiological sensitivities."""
    insights: List[Insight] = []
    if not preferences:
        return insights

    sensitivities = set(preferences.sensitivities)

    # 1. Heat Sensitivity
    heat_thresh = 35.0 if units == "metric" else 95.0
    if "heat" in sensitivities and (current.feels_like >= heat_thresh or current.temp >= heat_thresh):
        insights.append(
            Insight(
                title="Extreme Heat Caution",
                message=f"Feels like {current.feels_like}°. UV and heat levels are heightened. Stay in shaded or air-conditioned environments and hydrate regularly.",
                severity="warning",
                icon="sun",
                relevance_score=99,
                category="health",
            )
        )

    # 2. Cold Sensitivity
    cold_thresh = 14.0 if units == "metric" else 57.0
    if "cold" in sensitivities and current.temp <= cold_thresh:
        insights.append(
            Insight(
                title="Cold Weather Sensitivity Notice",
                message=f"Brisk {current.temp}° with wind speed of {current.wind_speed} {'km/h' if units == 'metric' else 'mph'}. Wear thermal layers before stepping out.",
                severity="caution",
                icon="snowflake",
                relevance_score=87,
                category="health",
            )
        )

    # 3. Respiratory / Allergies Sensitivity
    if "allergies" in sensitivities and metrics.aqi > 90:
        insights.append(
            Insight(
                title="Air Quality & Allergy Advisory",
                message=f"AQI is {metrics.aqi} ({metrics.aqi_level}). Airborne particulates may cause eye or respiratory irritation. Wearing an N95 mask is suggested.",
                severity="warning" if metrics.aqi >= 150 else "caution",
                icon="shield-alert",
                relevance_score=97 if metrics.aqi >= 150 else 89,
                category="health",
            )
        )

    # 4. Rain Sensitivity
    if "rain" in sensitivities:
        near_term_rain = max((h.precipitation_prob for h in hourly[:6]), default=0)
        if near_term_rain >= 30:
            insights.append(
                Insight(
                    title="Rain Sensitivity Precaution",
                    message=f"{near_term_rain}% chance of damp weather within the next few hours. Waterproof footwear and outerwear recommended.",
                    severity="caution",
                    icon="umbrella",
                    relevance_score=84,
                    category="health",
                )
            )

    return insights


def generate_generic_fallback_insights(
    current: CurrentWeather,
    daily: List[DailyForecastItem],
    metrics: KeyMetrics,
    units: str,
) -> List[Insight]:
    """Fallback insights generated for anonymous or newly onboarding users."""
    fallbacks: List[Insight] = []

    # UV advisory
    if metrics.uv_index >= 6.0:
        fallbacks.append(
            Insight(
                title="High UV Exposure Today",
                message=f"UV Index reaches {metrics.uv_index} ({metrics.uv_level}). Sun protection (SPF 30+ and sunglasses) recommended between 11:00 AM and 3:30 PM.",
                severity="caution",
                icon="sun",
                relevance_score=75,
                category="general",
            )
        )

    # Air quality advisory
    if metrics.aqi > 100:
        fallbacks.append(
            Insight(
                title="Moderate to Poor Air Quality",
                message=f"Current AQI is {metrics.aqi} ({metrics.aqi_level}). Sensitive groups should limit prolonged outdoor exertion.",
                severity="caution",
                icon="shield-alert",
                relevance_score=78,
                category="general",
            )
        )

    # Golden hour & Sunset
    if current.sunset:
        fallbacks.append(
            Insight(
                title="Sunset & Golden Hour",
                message=f"Sunset occurs at {current.sunset}. Expect calm twilight conditions for evening walks.",
                severity="info",
                icon="sun",
                relevance_score=50,
                category="general",
            )
        )

    # Temperature difference
    if daily:
        swing = round(daily[0].temp_max - daily[0].temp_min, 1)
        if swing >= (10.0 if units == "metric" else 18.0):
            fallbacks.append(
                Insight(
                    title=f"Significant Daily Temp Range ({swing}°)",
                    message=f"Expect a swing from a low of {daily[0].temp_min}° to a high of {daily[0].temp_max}°. Dressing in layers is advised.",
                    severity="info",
                    icon="compass",
                    relevance_score=55,
                    category="general",
                )
            )

    # Rain advisory
    if daily and daily[0].precipitation_prob >= 40:
        fallbacks.append(
            Insight(
                title="Precipitation Expected Today",
                message=f"There is a {daily[0].precipitation_prob}% probability of rain today. Keep an umbrella accessible.",
                severity="advice",
                icon="umbrella",
                relevance_score=70,
                category="general",
            )
        )

    return fallbacks


def personalize_insights(
    preferences: Optional[UserPreferenceBase],
    current: CurrentWeather,
    hourly: List[HourlyForecastItem],
    daily: List[DailyForecastItem],
    metrics: KeyMetrics,
    units: str = "metric",
) -> Tuple[List[Insight], List[Insight]]:
    """Synthesize and prioritize weather insights based on user profile.

    Returns:
        (top_3_insights, all_ranked_insights)
    """
    all_insights: List[Insight] = []

    # Evaluate specialized rule sets
    all_insights.extend(evaluate_commute_insights(preferences, hourly, units))
    all_insights.extend(evaluate_farming_insights(preferences, current, hourly, daily, units))
    all_insights.extend(evaluate_fitness_insights(preferences, current, hourly, metrics, units))
    all_insights.extend(evaluate_travel_insights(preferences, daily, units))
    all_insights.extend(evaluate_sensitivities_insights(preferences, current, hourly, metrics, units))

    # Add generic fallbacks if insight count is low or for anonymous users
    fallback_candidates = generate_generic_fallback_insights(current, daily, metrics, units)
    existing_titles = {ins.title for ins in all_insights}
    for fb in fallback_candidates:
        if fb.title not in existing_titles:
            all_insights.append(fb)

    # De-duplicate by title while keeping highest relevance score
    unique_insights_map = {}
    for ins in all_insights:
        if ins.title not in unique_insights_map or ins.relevance_score > unique_insights_map[ins.title].relevance_score:
            unique_insights_map[ins.title] = ins

    # Rank sorted by relevance_score descending
    ranked_insights = sorted(unique_insights_map.values(), key=lambda x: x.relevance_score, reverse=True)

    top_3 = ranked_insights[:3]
    return top_3, ranked_insights
