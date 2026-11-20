from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user_schema import UserCreate, UserLogin, UserResponse
from services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user)

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login_user(db, credentials)
