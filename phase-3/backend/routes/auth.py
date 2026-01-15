from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import Optional
from datetime import timedelta
import re

from auth import create_access_token, validate_email_format, validate_password_strength
from models import UserCreate, UserRead, User
from db import get_session
from services.user_service import UserService
from utils.logging import get_app_logger

router = APIRouter()

security = HTTPBearer()

logger = get_app_logger()


@router.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user with comprehensive validation"""
    # Validate email format
    if not user.email:
        logger.warning("Registration attempt with empty email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    if not validate_email_format(user.email):
        logger.warning(f"Registration attempt with invalid email format: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    if not user.password:
        logger.warning(f"Registration attempt with empty password for email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )

    is_valid, error_msg = validate_password_strength(user.password)
    if not is_valid:
        logger.warning(f"Registration attempt with weak password for email: {user.email} - {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Validate name if provided
    if user.name and len(user.name.strip()) == 0:
        logger.warning(f"Registration attempt with whitespace-only name for email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name cannot be empty or whitespace only"
        )

    # Check if user already exists
    existing_user = UserService.get_user_by_email(session, user.email)
    if existing_user:
        logger.info(f"Registration attempt for existing email: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user using service
    try:
        db_user = UserService.create_user(session, user)
        logger.info(f"Successfully registered user: {user.email}")
    except Exception as e:
        logger.error(f"Error creating user {user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error"
        )

    # Convert to response model manually
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        created_at=db_user.created_at
    )


@router.post("/auth/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """Login user and return JWT token with comprehensive validation"""
    # Validate email format
    if not email:
        logger.warning("Login attempt with empty email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    if not validate_email_format(email):
        logger.warning(f"Login attempt with invalid email format: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password
    if not password:
        logger.warning(f"Login attempt with empty password for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )

    # Find user by email using service
    user = UserService.get_user_by_email(session, email)

    if not user:
        logger.info(f"Login attempt for non-existent email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not UserService.verify_password(password, user.hashed_password):
        logger.warning(f"Login attempt with incorrect password for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.warning(f"Login attempt for inactive account: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name
    }
    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(days=7)  # Token valid for 7 days
    )

    logger.info(f"Successful login for user: {email}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        )
    }


@router.post("/auth/logout")
def logout():
    """Logout user (client-side token removal)"""
    logger.info("User logged out")
    return {"message": "Successfully logged out"}
