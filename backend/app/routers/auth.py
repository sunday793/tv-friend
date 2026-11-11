"""Authentication HTTP endpoints.

Defines the routes for user registration and login.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services import auth_service
from app.core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    """Register a new user and return an access token.

    Checks if the email or username is already taken. If not, creates
    the user and logs them in immediately.
    """
    if auth_service.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    if auth_service.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    user = auth_service.create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
    )

    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    """Authenticate a user and return an access token.

    Accepts form-data (username, password) as required by the OAuth2
    standard used by Swagger UI.
    """
    user = auth_service.authenticate_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)
