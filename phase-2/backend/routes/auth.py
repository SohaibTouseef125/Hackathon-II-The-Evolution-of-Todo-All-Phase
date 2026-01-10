from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import Optional
from datetime import timedelta

from auth import create_access_token
from models import UserCreate, UserRead, User
from db import get_session
from services.user_service import UserService

router = APIRouter()

security = HTTPBearer()


@router.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = UserService.get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user using service
    db_user = UserService.create_user(session, user)

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
    """Login user and return JWT token"""
    # Find user by email using service
    user = UserService.get_user_by_email(session, email)

    if not user or not UserService.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
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
    return {"message": "Successfully logged out"}
