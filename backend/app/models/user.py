"""User ORM model.

Represents an application user. Stores credentials required for
authentication (email, username, hashed password). Passwords are
never stored in plain text — see `app.core.security.hash_password`.

Relationships:
    watchlist: one-to-many with WatchlistItem (added in a later step).
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """Application user.

    Attributes:
        id: Primary key.
        email: Unique email address, used for login and notifications.
        username: Unique display name.
        hashed_password: argon2 hash of the user's password.
        is_active: Allows disabling an account without deleting it.
        created_at: Timestamp of account creation (from TimestampMixin).
        updated_at: Timestamp of the last update (from TimestampMixin).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    