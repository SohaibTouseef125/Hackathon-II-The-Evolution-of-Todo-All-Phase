from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, create_engine, select, Field
from sqlmodel.pool import StaticPool
from datetime import timedelta, datetime
from typing import Optional
import uuid
from jose import JWTError, jwt
import os
from passlib.context import CryptContext

# Models
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    user = session.exec(
        select(User).where(User.email == email)
    ).first()
    return user

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user"""
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create new user
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Create app
app = FastAPI(title="Todo API", version="1.0.0")

@app.post("/api/auth/register")
def register(user: UserCreate, session: Session = Depends(lambda: test_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = create_user(session, user)

    # Convert to response model manually
    return UserRead(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        created_at=db_user.created_at
    )

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(lambda: test_session)):
    """Login user and return JWT token"""
    # Extract email and password from form_data
    email = form_data.username  # OAuth2PasswordRequestForm uses 'username' field which corresponds to email in our case
    password = form_data.password

    # Find user by email
    user = get_user_by_email(session, email)

    if not user or not verify_password(password, user.hashed_password):
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

# Create in-memory database for testing
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

# Create a session for testing
with Session(engine) as session:
    test_session = session
    client = TestClient(app)

    # Test registration
    print("Testing registration...")
    response = client.post("/api/auth/register", json={
        "email": "login@example.com",
        "name": "Login User",
        "password": "securepassword"
    })
    print(f"Registration status: {response.status_code}")
    if response.status_code != 200:
        print(f"Registration error: {response.text}")
    else:
        print(f"Registration data: {response.json()}")

    # Test login
    print("\nTesting login...")
    response = client.post("/api/auth/login", data={
        "username": "login@example.com",  # Using username as email
        "password": "securepassword"
    })
    print(f"Login status: {response.status_code}")
    if response.status_code != 200:
        print(f"Login error: {response.text}")
    else:
        print(f"Login data: {response.json()}")

    # Debug: Check if user exists in database
    user_check = get_user_by_email(test_session, "login@example.com")
    print(f"\nDebug: User found in DB: {user_check is not None}")
    if user_check:
        print(f"User email: {user_check.email}")
        print(f"User name: {user_check.name}")
        print(f"Hashed password: {user_check.hashed_password[:20]}...")  # Just first 20 chars