"""ORM models for shows, persons, and watchlist items.

Defines the `Show` table, the `Person` table (actors), the `ShowCast`
association table (many-to-many between shows and persons), and the
`WatchlistItem` table (the association between a user and a show).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ShowCast(Base):
    """Association table between Shows and Persons.
    
    Stores the specific role or character name the person played
    in this particular show.
    """

    __tablename__ = "show_cast"

    show_id: Mapped[int] = mapped_column(
        ForeignKey("shows.id", ondelete="CASCADE"), primary_key=True
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"), primary_key=True
    )
    
    character_name: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Show(Base, TimestampMixin):
    """A TV series."""

    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    external_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    media_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Many-to-many relationship with Person through ShowCast
    cast: Mapped[list["Person"]] = relationship(
        secondary="show_cast", back_populates="shows"
    )

    watchlist_items: Mapped[list["WatchlistItem"]] = relationship(
        back_populates="show", cascade="all, delete-orphan"
    )


class Person(Base, TimestampMixin):
    """An actor or crew member."""

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    external_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Many-to-many relationship with Show through ShowCast
    shows: Mapped[list["Show"]] = relationship(
        secondary="show_cast", back_populates="cast"
    )


class WatchlistItem(Base, TimestampMixin):
    """An entry in a user's watchlist.

    Links a user to a show and tracks their personal status (e.g.
    "watching", "completed") and rating (1-10).
    """

    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    show_id: Mapped[int] = mapped_column(
        ForeignKey("shows.id", ondelete="CASCADE"), nullable=False
    )
    
    status: Mapped[str] = mapped_column(String(50), default="watching", nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)

    user: Mapped["User"] = relationship(back_populates="watchlist")
    show: Mapped["Show"] = relationship(back_populates="watchlist_items")
