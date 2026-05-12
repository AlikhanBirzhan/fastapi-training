from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db, get_current_user
from app.models import User
from app.schemas import UserRegisterRequest, UserResponse, UserLoginRequest, TokenResponse
from app.service import users as users_service

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db, payload.login, payload.password)

@router.post("/auth/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    return users_service.login_user(db, payload.login, payload.password)

@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)