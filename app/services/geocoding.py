"""Geocoding service using Open-Meteo Geocoding API with local fallback."""

from typing import List
import httpx
from app.schemas import GeocodeCity

# Reliable fallback dataset for instant search and offline support
PRESET_CITIES: List[dict] = [
    {"name": "New Delhi", "state": "Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777},
    {"name": "Bengaluru", "state": "Karnataka", "country": "India", "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai", "state": "Tamil Nadu", "country": "India", "lat": 13.0827, "lon": 80.2707},
    {"name": "Kolkata", "state": "West Bengal", "country": "India", "lat": 22.5726, "lon": 88.3639},
    {"name": "Hyderabad", "state": "Telangana", "country": "India", "lat": 17.3850, "lon": 78.4867},
    {"name": "Pune", "state": "Maharashtra", "country": "India", "lat": 18.5204, "lon": 73.8567},
    {"name": "Ahmedabad", "state": "Gujarat", "country": "India", "lat": 23.0225, "lon": 72.5714},
    {"name": "Jaipur", "state": "Rajasthan", "country": "India", "lat": 26.9124, "lon": 75.7873},
    {"name": "Coimbatore", "state": "Tamil Nadu", "country": "India", "lat": 11.0168, "lon": 76.9558},
    {"name": "Chandigarh", "state": "Punjab", "country": "India", "lat": 30.7333, "lon": 76.7794},
    {"name": "London", "state": "England", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278},
    {"name": "New York", "state": "New York", "country": "United States", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "state": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503},
    {"name": "Dubai", "state": "Dubai", "country": "United Arab Emirates", "lat": 25.2048, "lon": 55.2708},
]


async def search_cities(query: str, limit: int = 6) -> List[GeocodeCity]:
    """Search cities matching query string from Open-Meteo or fallback presets."""
    q = query.strip()
    if not q or len(q) < 2:
        return []

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": q,
        "count": limit,
        "language": "en",
        "format": "json"
    }

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            res = await client.get(url, params=params)
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])
                if results:
                    return [
                        GeocodeCity(
                            id=item.get("id"),
                            name=item.get("name", "Unknown"),
                            state=item.get("admin1"),
                            country=item.get("country", "Unknown"),
                            lat=float(item.get("latitude", 0.0)),
                            lon=float(item.get("longitude", 0.0)),
                        )
                        for item in results[:limit]
                    ]
    except Exception:
        pass

    # Filter preset list if external API failed or had no results
    q_lower = q.lower()
    matched = [
        GeocodeCity(**city)
        for city in PRESET_CITIES
        if q_lower in city["name"].lower() or (city["state"] and q_lower in city["state"].lower())
    ]
    return matched[:limit]
