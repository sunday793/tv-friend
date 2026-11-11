"""API routers package.

Contains FastAPI APIRouter instances that define the HTTP endpoints
of the application.
"""

from fastapi import APIRouter

from app.routers import auth, shows

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(shows.router)
