"""Database connection and session management.

Creates the SQLAlchemy engine bound to the PostgreSQL database and a
session factory (`SessionLocal`). Provides the `get_db` dependency
that FastAPI routers use to obtain a database session per request.

Engine options:
    - pool_pre_ping: verifies connections before use, avoiding stale
      connection errors after long idle periods.
    - echo: prints SQL statements to stdout when DEBUG is enabled.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed afterwards.

    Used as a FastAPI dependency:

        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: An open SQLAlchemy session bound to the engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        