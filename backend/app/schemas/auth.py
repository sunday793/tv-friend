"""Authentication schemas.

Pydantic models for the /api/auth endpoints:
    - RegisterRequest: body of the registration request.
    - LoginRequest: body for JSON-based login (kept for flexibility).
    - TokenResponse: response containing the JWT access token.
    - CurrentUser: minimal representation of the authenticated user.

These schemas are independent of the ORM User model: they define what
the API accepts and returns, not what is stored in the database.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    """Request body for user registration.

    Attributes:
        email: Valid email address, must be unique across users.
        username: Display name, must be unique across users.
        password: Plain-text password. Minimum length is enforced here;
            hashing happens later in the auth service.
    """

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    """Request body for JSON-based login.

    Note: the primary login endpoint uses OAuth2PasswordRequestForm
    (form-data), which is required by FastAPI's security utilities.
    This schema exists for cases where a JSON login is more convenient,
    e.g. custom clients or tests.
    """

    username: str
    password: str


class TokenResponse(BaseModel):
    """Response containing a JWT access token.

    Attributes:
        access_token: The signed JWT string.
        token_type: Always "bearer" for OAuth2-compatible clients.
    """

    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    """Minimal representation of the authenticated user.

    Returned by /api/users/me and embedded in some auth responses.
    Never exposes password hashes or other sensitive fields.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    is_active: bool
    