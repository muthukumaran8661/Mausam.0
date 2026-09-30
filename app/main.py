"""Main FastAPI application entry point for Mausam."""

import time
from collections import defaultdict
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.routers import home, users, cities, alerts

settings = get_settings()

# In-memory sliding window IP rate limiter
_rate_limits = defaultdict(list)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifespan handler."""
    init_db()
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


# Mount static assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Mount Routers
app.include_router(home.router)
app.include_router(users.router)
app.include_router(cities.router)
app.include_router(alerts.router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
        "timestamp": time.time(),
    }
