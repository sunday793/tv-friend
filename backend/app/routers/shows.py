"""HTTP endpoints for searching media and managing watchlists."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.show import (
    MediaSearchResult,
    WatchlistAddRequest,
    WatchlistItemRead,
    WatchlistUpdateRequest,
    ShowDetailsRead,
)
from app.services import kinopoisk_client, show_service

router = APIRouter(prefix="/api/shows", tags=["shows"])


@router.get("/search", response_model=list[MediaSearchResult])
def search_media(query: str):
    """Search for movies, series, or shows by keyword.
    
    This endpoint queries the external API (Kinopoisk) and returns results
    without saving them to our database. To save an item, use the
    /watchlist endpoint.
    """
    try:
        return show_service.search_media(query)
    except kinopoisk_client.KinopoiskAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )


@router.get("/watchlist", response_model=list[WatchlistItemRead])
def get_watchlist(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Retrieve the authenticated user's watchlist."""
    return show_service.get_user_watchlist(db, current_user)


@router.post("/watchlist", response_model=WatchlistItemRead, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    request: WatchlistAddRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Add a media item to the watchlist.
    
    If the media is not yet in our database, it will be fetched from
    the external API and saved automatically.
    """
    try:
        return show_service.add_to_watchlist(db, current_user, request.external_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except kinopoisk_client.KinopoiskAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )


@router.patch("/watchlist/{item_id}", response_model=WatchlistItemRead)
def update_watchlist_item(
    item_id: int,
    request: WatchlistUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update the status or rating of a media item in the watchlist."""
    try:
        return show_service.update_watchlist_item(
            db, current_user, item_id, status=request.status, rating=request.rating
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/watchlist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Remove a media item from the watchlist."""
    try:
        show_service.remove_from_watchlist(db, current_user, item_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{external_id}", response_model=ShowDetailsRead)
def get_media_details(
    external_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    """Get detailed information about a specific media, including cast.
    
    If the media is not in our database, it will be fetched from the API.
    """
    try:
        return show_service.get_or_create_show(db, external_id)
    except kinopoisk_client.KinopoiskAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )
    