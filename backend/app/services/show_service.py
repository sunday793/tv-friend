"""Service for managing media (shows, movies) and user watchlists.

Coordinates between the database, the external API client, and the
routers. Handles caching (saving fetched media to the local DB) and
watchlist management.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.show import Show, WatchlistItem
from app.models.user import User
from app.services import kinopoisk_client
from app.services.kinopoisk_client import KinopoiskAPIError


def search_media(query: str) -> list[kinopoisk_client.ExternalMedia]:
    """Search for media using the external API.

    This does not save anything to the database. It is just a proxy
    to the Kinopoisk client so routers don't need to know which
    external API is being used.

    Args:
        query: The search string.

    Returns:
        A list of neutral ExternalMedia objects.
    """
    return kinopoisk_client.search_media(query)


def get_or_create_show(db: Session, external_id: str, source: str = "kinopoisk") -> Show:
    """Get a show from the database, or fetch and create it if missing.

    Args:
        db: Active database session.
        external_id: The ID of the media in the external API.
        source: The name of the external API (default "kinopoisk").

    Returns:
        The existing or newly created Show object.

    Raises:
        KinopoiskAPIError: If the media is not in the DB and the API fails.
    """
    # 1. Try to find it in our DB first
    stmt = select(Show).where(
        Show.source == source,
        Show.external_id == external_id
    )
    existing_show = db.execute(stmt).scalar_one_or_none()
    
    if existing_show:
        return existing_show

    # 2. If not found, fetch from external API
    external_media = kinopoisk_client.get_media_details(external_id)

    # 3. Save to DB
    new_show = Show(
        source=source,
        external_id=external_media.external_id,
        media_type=external_media.type,
        title=external_media.title,
        year=external_media.year,
        poster_url=external_media.poster_url,
        overview=external_media.overview,
    )
    db.add(new_show)
    db.commit()
    db.refresh(new_show)
    
    return new_show


def add_to_watchlist(db: Session, user: User, external_id: str) -> WatchlistItem:
    """Add a media item to the user's watchlist.

    If the media is not yet in the local database, it is fetched from
    the external API and saved first.

    Args:
        db: Active database session.
        user: The authenticated user.
        external_id: The ID of the media in the external API.

    Returns:
        The newly created WatchlistItem.

    Raises:
        ValueError: If the media is already in the user's watchlist.
    """
    # 1. Ensure the show exists in our DB
    show = get_or_create_show(db, external_id)

    # 2. Check if it's already in the user's watchlist
    stmt = select(WatchlistItem).where(
        WatchlistItem.user_id == user.id,
        WatchlistItem.show_id == show.id
    )
    existing_item = db.execute(stmt).scalar_one_or_none()
    
    if existing_item:
        raise ValueError("Media is already in the watchlist")

    # 3. Create the watchlist item
    item = WatchlistItem(
        user_id=user.id,
        show_id=show.id,
        status="planned", # Default status
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item


def get_user_watchlist(db: Session, user: User) -> list[WatchlistItem]:
    """Retrieve all watchlist items for a specific user.

    Args:
        db: Active database session.
        user: The authenticated user.

    Returns:
        A list of WatchlistItem objects, ordered by date added.
    """
    stmt = (
        select(WatchlistItem)
        .where(WatchlistItem.user_id == user.id)
        .order_by(WatchlistItem.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


def update_watchlist_item(
    db: Session, 
    user: User, 
    item_id: int, 
    status: str | None = None, 
    rating: int | None = None
) -> WatchlistItem:
    """Update the status or rating of a watchlist item.

    Args:
        db: Active database session.
        user: The authenticated user (ensures they own the item).
        item_id: The ID of the WatchlistItem to update.
        status: The new status (optional).
        rating: The new rating (optional).

    Returns:
        The updated WatchlistItem.

    Raises:
        ValueError: If the item is not found or does not belong to the user.
    """
    stmt = select(WatchlistItem).where(
        WatchlistItem.id == item_id,
        WatchlistItem.user_id == user.id
    )
    item = db.execute(stmt).scalar_one_or_none()

    if not item:
        raise ValueError("Watchlist item not found")

    if status is not None:
        item.status = status
    if rating is not None:
        item.rating = rating

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_from_watchlist(db: Session, user: User, item_id: int) -> None:
    """Remove an item from the user's watchlist.

    Args:
        db: Active database session.
        user: The authenticated user (ensures they own the item).
        item_id: The ID of the WatchlistItem to delete.

    Raises:
        ValueError: If the item is not found or does not belong to the user.
    """
    stmt = select(WatchlistItem).where(
        WatchlistItem.id == item_id,
        WatchlistItem.user_id == user.id
    )
    item = db.execute(stmt).scalar_one_or_none()

    if not item:
        raise ValueError("Watchlist item not found")

    db.delete(item)
    db.commit()
