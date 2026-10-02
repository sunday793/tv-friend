"""Security utilities: password hashing and JWT token handling.

Provides functions for:
    - Hashing passwords before storing them in the database.
    - Verifying a plain password against a stored hash.
    - Creating signed JWT access tokens containing the user id.
    - Decoding and validating JWT tokens.

Uses pwdlib with bcrypt for password hashing and python-jose for JWT.
The signing algorithm and secret key are read from application settings.
"""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        A bcrypt hash as a string, safe to store in the database.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether a plain password matches a stored hash.

    Args:
        plain_password: The password entered by the user.
        hashed_password: The bcrypt hash stored in the database.

    Returns:
        True if the password matches, False otherwise.
    """
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """Create a signed JWT access token for a given user.

    The token payload contains the user id in the "sub" claim and an
    expiration timestamp in the "exp" claim. Lifetime is controlled by
    the ACCESS_TOKEN_EXPIRE_MINUTES setting.

    Args:
        user_id: The primary key of the user the token belongs to.

    Returns:
        An encoded JWT string.
    """
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> int | None:
    """Decode a JWT token and return the user id from its "sub" claim.

    Validates the signature and the expiration time. Returns None if the
    token is invalid, expired, or does not contain a valid user id.

    Args:
        token: The encoded JWT string.

    Returns:
        The user id as an integer, or None if the token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except (JWTError, ValueError):
        return None