"""Base class and shared mixins for all ORM models.

Defines `Base` — the declarative base every model inherits from — and
`TimestampMixin`, which adds `created_at` and `updated_at` columns
managed automatically by the database.

SQLAlchemy 2.0 style is used throughout: columns are declared with
`Mapped[...]` type annotations and `mapped_column(...)`.
"""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base for all ORM models in the project.

    Every model inherits from this class. Alembic uses `Base.metadata`
    to discover tables and generate migrations.
    """


class TimestampMixin:
    """Mixin that adds `created_at` and `updated_at` columns.

    Both columns are populated by the database server:
        - created_at: set once on insert.
        - updated_at: updated automatically on every UPDATE.

    Using `server_default` and `onupdate` keeps the values consistent
    even when rows are modified outside the ORM.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    