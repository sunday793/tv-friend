"""Client for the Kinopoisk Unofficial API.

Encapsulates all HTTP communication with kinopoiskapiunofficial.tech.
Returns neutral Python dataclasses instead of raw JSON dictionaries,
so the rest of the application (services, routers) does not depend
on the external API's structure.
"""

from dataclasses import dataclass

import httpx

from app.config import settings


@dataclass
class ExternalMedia:
    """Neutral representation of media (movie, series, anime, etc.)."""

    external_id: str
    title: str
    type: str  # e.g., "FILM", "TV_SERIES", "MINI_SERIES", "TV_SHOW"
    year: int | None
    poster_url: str | None
    overview: str | None


class KinopoiskAPIError(Exception):
    """Raised when the Kinopoisk API returns an error or is unreachable."""

    pass


def _get_headers() -> dict[str, str]:
    """Construct standard headers required by the Kinopoisk API."""
    return {
        "X-API-KEY": settings.KINOPOISK_API_KEY,
        "Content-Type": "application/json",
    }


def _parse_year(year_str: str | int | None) -> int | None:
    """Safely parse a year value from the API to an integer."""
    if not year_str:
        return None
    try:
        return int(year_str)
    except (ValueError, TypeError):
        return None


def search_media(query: str) -> list[ExternalMedia]:
    """Search for any media type by keyword.

    Args:
        query: The search string (e.g., "Breaking Bad").

    Returns:
        A list of ExternalMedia objects matching the query.

    Raises:
        KinopoiskAPIError: If the request fails or returns a bad status.
    """
    url = f"{settings.KINOPOISK_BASE_URL}/api/v2.1/films/search-by-keyword"
    params = {"keyword": query, "page": 1}

    try:
        with httpx.Client() as client:
            response = client.get(url, headers=_get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as e:
        raise KinopoiskAPIError(f"Failed to search media: {e}") from e

    results = []
    for item in data.get("films", []):
        # We keep all types: FILM, TV_SERIES, TV_SHOW, etc.
        results.append(
            ExternalMedia(
                external_id=str(item["filmId"]),
                title=item.get("nameRu") or item.get("nameEn") or "Unknown",
                type=item.get("type", "UNKNOWN"),
                year=_parse_year(item.get("year")),
                poster_url=item.get("posterUrl"),
                overview=item.get("description"),
            )
        )
    return results


def get_media_details(external_id: str) -> ExternalMedia:
    """Fetch detailed information about specific media.

    Args:
        external_id: The Kinopoisk ID.

    Returns:
        An ExternalMedia object with full details.

    Raises:
        KinopoiskAPIError: If the request fails or the media is not found.
    """
    url = f"{settings.KINOPOISK_BASE_URL}/api/v2.2/films/{external_id}"

    try:
        with httpx.Client() as client:
            response = client.get(url, headers=_get_headers())
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as e:
        raise KinopoiskAPIError(f"Failed to fetch media {external_id}: {e}") from e

    return ExternalMedia(
        external_id=str(data["kinopoiskId"]),
        title=data.get("nameRu") or data.get("nameOriginal") or "Unknown",
        type=data.get("type", "UNKNOWN"),
        year=_parse_year(data.get("year")),
        poster_url=data.get("posterUrl"),
        overview=data.get("description"),
    )


@dataclass
class ExternalPerson:
    """Neutral representation of a person (actor)."""
    external_id: str
    name: str
    photo_url: str | None


@dataclass
class ExternalCastMember:
    """Association of a person to a show with a specific role."""
    person: ExternalPerson
    character_name: str | None


def get_show_cast(external_id: str) -> list[ExternalCastMember]:
    """Fetch the cast (actors) for a specific show.
    
    Note: On the free tier of the API, this might return an empty list
    or raise an error. We handle it gracefully.

    Args:
        external_id: The Kinopoisk ID of the show.

    Returns:
        A list of ExternalCastMember objects.

    Raises:
        KinopoiskAPIError: If the request fails or returns a bad status.
    """
    url = f"{settings.KINOPOISK_BASE_URL}/api/v2.2/films/{external_id}/staff"

    try:
        with httpx.Client() as client:
            response = client.get(url, headers=_get_headers())
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as e:
        # If the API returns 403/404, we might just return an empty list
        # instead of crashing the whole process.
        if getattr(e, "response", None) and e.response.status_code in (403, 404):
            return []
        raise KinopoiskAPIError(f"Failed to fetch cast for {external_id}: {e}") from e

    cast = []
    for item in data:
        # We are only interested in actors (professionKey == "ACTOR")
        if item.get("professionKey") != "ACTOR":
            continue
            
        person = ExternalPerson(
            external_id=str(item["staffId"]),
            name=item.get("nameRu") or item.get("nameEn") or "Unknown",
            photo_url=item.get("posterUrl"),
        )
        cast.append(
            ExternalCastMember(
                person=person,
                character_name=item.get("description"), # Usually the role name
            )
        )
    return cast
