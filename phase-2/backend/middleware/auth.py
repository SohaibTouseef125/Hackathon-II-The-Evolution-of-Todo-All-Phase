from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token_and_get_user_id(token: str) -> str:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """Check if the authenticated user owns the resource"""
    return str(user_id) == str(resource_user_id)


def validate_user_access(token: str, resource_user_id: str) -> bool:
    """Validate that the user has access to the resource"""
    authenticated_user_id = verify_token_and_get_user_id(token)
    return check_user_owns_resource(authenticated_user_id, resource_user_id)