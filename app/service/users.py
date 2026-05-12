from fastapi import HTTPException
from sqlalchemy.orm import Session
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.repository import users as users_repository
from app.schemas import UserResponse, TokenResponse
import os

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(login: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": login, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_user(db: Session, login: str, password: str) -> UserResponse:
    if users_repository.get_user(db, login):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(password)
    user = users_repository.create_user(db, login, hashed)
    db.commit()
    return UserResponse.model_validate(user)

def login_user(db: Session, login: str, password: str) -> TokenResponse:
    user = users_repository.get_user(db, login)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid login or password")
    token = create_access_token(login)
    return TokenResponse(access_token=token)