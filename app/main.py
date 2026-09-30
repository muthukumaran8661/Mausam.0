import sys
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure project root is in sys.path so 'app.*' imports work from any working directory
_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.routers import home, users, cities, alerts

settings = get_settings()

# Base directory for relative paths (app/)
BASE_DIR = Path(__file__).resolve().parent

# Mount templates using path relative to this file
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# In-memory sliding window IP rate limiter
_rate_limits = defaultdict(list)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifespan handler."""
    init_db()
    # Auto-seed demo data on first startup (safe: checks for existing user)
    try:
        from seed import seed_database  # noqa: PLC0415
        seed_database()
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("Seed skipped: %s", exc)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Mausam: Personalized Mobile-First Weather Application with Smart Human Insights",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limit API endpoints based on client IP."""
    if request.url.path.startswith("/api/"):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        window_start = now - 60.0

        # Purge timestamps older than 1 minute
        _rate_limits[client_ip] = [t for t in _rate_limits[client_ip] if t > window_start]

        if len(_rate_limits[client_ip]) >= settings.rate_limit_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Too many requests. Please slow down."},
            )

        _rate_limits[client_ip].append(now)

    response = await call_next(request)
    return response


# Mount static assets relative to this file
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Mount Routers
app.include_router(home.router)
app.include_router(users.router)
app.include_router(cities.router)
app.include_router(alerts.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
