"""Pydantic schemas for media (shows, movies) and watchlists.

Defines the data structures for search results and watchlist responses.
"""

from pydantic import BaseModel, ConfigDict, Field


class MediaSearchResult(BaseModel):
    """A single item returned by the search endpoint.

    Mirrors the ExternalMedia dataclass from the Kinopoisk client.
    """

    external_id: str
    title: str
    type: str
    year: int | None = None
    poster_url: str | None = None
    overview: str | None = None


class WatchlistAddRequest(BaseModel):
    """Request body to add a media item to the watchlist."""

    external_id: str = Field(description="The ID of the media from the external API")


class WatchlistItemRead(BaseModel):
    """A watchlist entry returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    rating: int | None = None
    
    # Instead of returning just the DB id, we return the full nested show object
    show: "ShowRead"


class ShowRead(BaseModel):
    """Nested representation of a show inside the watchlist."""

    model_config = ConfigDict(from_attributes=True)

    external_id: str
    title: str
    media_type: str
    year: int | None = None
    poster_url: str | None = None
    overview: str | None = None
    