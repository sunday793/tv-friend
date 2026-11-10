"""Authentication service.

Contains business logic for user registration and login. This module
does not know anything about HTTP: it receives plain data (via schemas),
interacts with the database, and returns ORM objects or raises custom
exceptions that routers can translate into HTTP responses.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


def get_user_by_username(db: Session, username: str) -> User | None:
    """Fetch a user by their username.

    Args:
        db: Active database session.
        username: The username to look up.

    Returns:
        The User object if found, otherwise None.
    """
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetch a user by their email address.

    Args:
        db: Active database session.
        email: The email address to look up.

    Returns:
        The User object if found, otherwise None.
    """
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, email: str, username: str, password: str) -> User:
    """Create a new user in the database.

    Hashes the plain-text password before storing the user.

    Args:
        db: Active database session.
        email: The new user's email address.
        username: The new user's display name.
        password: The new user's plain-text password.

    Returns:
        The newly created and refreshed User object.
    """
    hashed_pwd = hash_password(password)
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_pwd,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """Authenticate a user by checking their username and password.

    Args:
        db: Active database session.
        username: The username provided during login.
        password: The plain-text password provided during login.

    Returns:
        The User object if authentication succeeds, otherwise None.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user