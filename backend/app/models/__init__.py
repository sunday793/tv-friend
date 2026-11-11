"""SQLAlchemy ORM models package.

All ORM models must be imported here so that Alembic's autogenerate
feature can detect them when producing migrations. If a model is not
imported in this file, Alembic will not see it.
"""

from app.models.base import Base
from app.models.user import User
from app.models.show import Show, WatchlistItem, Person, ShowCast

__all__ = ["Base", "User", "Show", "WatchlistItem", "Person", "ShowCast"]