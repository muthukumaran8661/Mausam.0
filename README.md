# Mausam (मौसम) — Personalized Mobile-First Weather Application

Mausam is a mobile-first weather web application with a Python backend and lightweight PWA frontend. Instead of overwhelming users with raw numbers, Mausam delivers smart, contextual human insights tailored to the user's location, daily commute times, farming/fitness/travel interests, and weather sensitivities (heat, cold, allergies/AQI, rain).

---

## Features

- **Dynamic Weather-Reactive Hero Card**: Ambient gradient dynamically adapts based on conditions and day/night (Clear Sky, Rainy Blue, Thunderstorm Purple, Mist/Overcast).
- **Personalized Smart Insights Engine (`services/personalization.py`)**: Pure function rule engine providing ranked actionable insights (e.g. *"Carry an umbrella for your evening commute (rain chance 65% at 6 PM)"*, *"Prime Outdoor Running Window at 07:00 with AQI 42"*).
- **Hourly 24h & 7-Day Forecast**: Horizontally scrollable 24-hour card rail and compact 7-day forecast with horizontal min/max temperature gradient bars.
- **Key Metrics Bento Grid**: Humidity, Wind speed & directional compass, UV Index with danger badges, Air Quality Index (AQI) with color-coded health indicators, Visibility, Barometric Pressure, and Sunrise/Sunset times.
- **Severe Weather Alerts Banner**: Color-coded (Red/Amber/Yellow) dismissible alert banner with notification badge.
- **Saved Cities Mini-Cards Rail**: Quick switch between favorite locations with live/cached temperature and condition overview, plus an integrated city search modal with live geocoding autocomplete.
- **Lifestyle & Interest Card**: Real-time actionable guidance tailored to active user interests (Commute, Fitness, Farming, Travel).
- **Full PWA Capabilities**:
  - `manifest.js`: Dynamically generates blob manifest with standalone mode, icons, shortcuts, and theme colors.
  - `service-worker.js`: Cache-first for App Shell assets, Network-first with cache fallback for `/api/*` data endpoints, offline fallback handling.
  - Offline banner notification with retry connection button.
- **Multilingual Support (i18n)**: Instant client-side localization for English (`en`), Hindi (`hi` / हिंदी), and Tamil (`ta` / தமிழ்).
- **Resilient Caching (`services/cache.py`)**: 10-minute in-memory TTL cache with stale-while-revalidate fallback displaying an `"Updated X min ago"` chip if network drops or upstream provider fails.

---

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy 2.0 + SQLite, HTTPX, Cachetools, Python-Dotenv
- **Weather Provider**: Open-Meteo API (free, open, no API key required) behind an abstract `BaseWeatherProvider` interface with realistic synthetic fallback
- **Frontend**: Jinja2 templates + Vanilla HTML5/CSS3/JavaScript (mobile-first responsive at 360px–390px, touch targets $\ge 44\text{px}$)
- **Testing**: Pytest, Pytest-Asyncio, Starlette TestClient

---

## Project Structure

```
SIH-26Mausam/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application, lifespan, static mounting, rate limiter, CORS
│   ├── config.py                   # Pydantic Settings configuration
│   ├── database.py                 # SQLAlchemy 2.0 SQLite engine & session management
│   ├── models.py                   # ORM models (User, UserPreference, SavedCity)
│   ├── schemas.py                  # Pydantic v2 validation models
│   ├── routers/
│   │   ├── home.py                 # GET / (HTML template) & GET /api/home (Aggregated JSON)
│   │   ├── users.py                # GET/PUT /api/users/{id}/preferences
│   │   ├── cities.py               # GET/POST/DELETE /api/users/{id}/cities & GET /api/geocode
│   │   └── alerts.py               # GET /api/alerts
│   ├── services/
│   │   ├── weather_provider.py     # BaseWeatherProvider ABC + OpenMeteoWeatherProvider
│   │   ├── personalization.py      # Pure function personalization rule engine
│   │   ├── geocoding.py            # City lookup with local fallback presets
│   │   └── cache.py                # 10-minute TTL in-memory cache + stale fallback
│   ├── templates/
│   │   └── index.html              # Mobile-first semantic template
│   └── static/
│       ├── manifest.js             # Dynamic PWA manifest blob injector & SW registration
│       ├── service-worker.js       # Cache-first App Shell + Network-first API
│       ├── app.js                  # Dynamic client logic, i18n, city switcher, modals
│       ├── styles.css              # Custom property design tokens, dark/light themes, animations
│       ├── offline.html            # Offline fallback page
│       └── icons/                  # 192x192, 512x512, maskable icons and SVGs
├── tests/
│   ├── test_personalization.py     # Comprehensive unit tests for personalization rules
│   ├── test_cache.py               # TTL cache and stale fallback tests
│   ├── test_weather_provider.py    # Open-Meteo parser and error handling tests
│   └── test_api.py                 # Endpoint integration tests
├── seed.py                         # Demo user seed script (Rahul Sharma with Delhi, Bengaluru, Mumbai)
├── requirements.txt                # Project dependencies
├── .env.example                    # Environment variable template
└── README.md
```

---

## Getting Started

### 1. Prerequisites
- Python 3.11 or higher
- Git

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd SIH-26Mausam

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file (or copy from `.env.example`):
```env
APP_NAME="Mausam"
ENVIRONMENT="development"
DEBUG=True
PORT=8000
DATABASE_URL="sqlite:///./mausam.db"
WEATHER_CACHE_TTL=600
CORS_ORIGINS="*"
RATE_LIMIT_PER_MINUTE=120
```

### 4. Database Initialization & Seeding
Run the seed script to create the SQLite database and seed demo user **Rahul Sharma** with initial preferences and saved cities (New Delhi, Bengaluru, Mumbai):
```bash
python seed.py
```

### 5. Running the Application
Launch the Uvicorn server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
Open your browser and navigate to:
**http://localhost:8000**

---

## Running Automated Tests

Run the complete test suite with verbose output:
```bash
python -m pytest -v
```
All 23 automated tests cover:
- Personalization rules (commute windows, farming spray/frost/irrigation, fitness running/AQI, travel weekend weather, heat/cold/allergy sensitivities, and generic fallbacks)
- In-memory cache behavior (TTL hit/miss, stale-while-revalidate fallback)
- Weather provider parsing, WMO code mapping, AQI evaluation, and cardinal directions
- FastAPI endpoints (`/health`, `/api/users/*`, `/api/cities`, `/api/geocode`, `/api/alerts`, `/api/home`)

---

## API Documentation

When the application is running in debug mode, interactive OpenAPI documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

Key endpoints:
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Rendered mobile-first HTML homepage |
| `GET` | `/api/home?user_id=&lat=&lon=&city_name=` | Aggregated weather, insights, alerts, and saved cities |
| `GET` | `/api/users/{id}/preferences` | Fetch user settings (units, language, interests, sensitivities) |
| `PUT` | `/api/users/{id}/preferences` | Update user settings and commute times |
| `GET` | `/api/users/{id}/cities` | List saved cities for a user |
| `POST` | `/api/users/{id}/cities` | Add a new city to saved locations |
| `DELETE` | `/api/users/{id}/cities/{city_id}` | Remove a saved city |
| `GET` | `/api/geocode?q={city}` | Search locations with coordinates |
| `GET` | `/api/alerts?lat=&lon=` | Retrieve active severe meteorological alerts |
| `GET` | `/health` | Application health check |

---

## Deploy on Render

Mausam is configured for deployment on [Render](https://render.com) as a Python Web Service.

> [!IMPORTANT]
> **Runtime Selection**: Create the service as Python 3 (or use Blueprint with `render.yaml`). The runtime cannot be changed after a service is created. If the service was created as Node, delete it and recreate it as a Python Web Service.

### Quick Deploy via Blueprint (Recommended)
1. Push your repository to GitHub.
2. In the Render Dashboard, click **New +** > **Blueprint**.
3. Connect your repository. Render will automatically read [`render.yaml`](render.yaml) and configure the service.

### Manual Web Service Configuration
If creating a Web Service manually in Render:

- **Name**: `mausam`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path**: `/health`

#### Environment Variables
| Variable | Value | Description |
|---|---|---|
| `PYTHON_VERSION` | `3.11.9` | Pins Python 3.11 runtime |
| `DATABASE_URL` | `sqlite:///./mausam.db` | Database connection URL |
| `ENVIRONMENT` | `production` | Production environment flag |
| `DEBUG` | `False` | Disables debug mode in production |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

> [!NOTE]
> **Database Persistence on Free Tier**: Render's free-tier disk is ephemeral — any changes written to local SQLite (`mausam.db`) will reset when the instance restarts or redeploys. For production data persistence, create a free Render PostgreSQL database and set the `DATABASE_URL` environment variable to your PostgreSQL connection string (`postgresql://...`). Mausam automatically connects to PostgreSQL when this variable is provided.

