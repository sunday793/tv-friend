"""FastAPI application entry point.

Creates the FastAPI app, configures CORS, and registers all routers.
This is the module that uvicorn runs (e.g. `uvicorn app.main:app --reload`).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth

app = FastAPI(
    title="TV Friend API",
    description="A TV tracker application API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "TV Friend API is running"}
