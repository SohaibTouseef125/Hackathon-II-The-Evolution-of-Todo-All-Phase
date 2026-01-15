from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import uuid
from sqlmodel import Session, select
import os
from dotenv import load_dotenv
import re

from models import UserRead, User
from db import get_session
from utils.logging import get_app_logger

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Initialize logger
logger = get_app_logger()

security = HTTPBearer()


def validate_email_format(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, ""


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token with validation"""
    # Validate the data being encoded
    user_id = data.get("sub")
    if not user_id:
        logger.error("Attempt to create token without user ID")
        raise ValueError("User ID is required to create access token")

    try:
        # Validate user_id format
        user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id
    except ValueError:
        logger.error(f"Invalid user ID format for token creation: {user_id}")
        raise ValueError("Invalid user ID format")

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    logger.info(f"Access token created for user: {user_uuid}")
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload with comprehensive validation"""
    try:
        # Basic validation of token
        if not token or len(token.strip()) == 0:
            logger.warning("Empty token provided for verification")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Some clients mistakenly include quotes around the token (e.g. Bearer "<token>")
        token = token.strip().strip('"').strip("'")

        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


        # Validate required claims
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Token missing required 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing required user information",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate token expiration
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            if datetime.utcnow() > datetime.utcfromtimestamp(exp_timestamp):
                logger.warning(f"Expired token attempted for user: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Validate issued at time
        iat_timestamp = payload.get("iat")
        if iat_timestamp:
            issued_at = datetime.utcfromtimestamp(iat_timestamp)
            if issued_at > datetime.utcnow():
                logger.warning(f"Token issued in the future for user: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token was issued in the future",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        logger.info(f"Token verified successfully for user: {user_id}")
        return payload

    except JWTError as e:
        logger.error(f"JWT verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error occurred",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)) -> UserRead:
    """Get current user from JWT token with comprehensive validation"""
    token = credentials.credentials
    payload = verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        logger.error("Token payload missing user ID")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - missing user information",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the user from the database to get complete information
    try:
        # Try to parse the user_id as UUID
        user_uuid = uuid.UUID(str(user_id)) if not isinstance(user_id, uuid.UUID) else user_id

        # Query the user from the database
        user = session.exec(select(User).where(User.id == user_uuid)).first()

        if not user:
            logger.warning(f"User not found in database: {user_uuid}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            logger.warning(f"Inactive user attempted authentication: {user_uuid}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Current user authenticated successfully: {user_uuid}")

        # Convert to UserRead response model
        return UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        )
    except ValueError:
        # If user_id is not a valid UUID
        logger.error(f"Invalid user ID format in token: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Error fetching user from database: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error occurred",
            headers={"WWW-Authenticate": "Bearer"},
        )
