from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.base import get_db
from app.core.config import settings
from app.core.security import create_access_token, decode_token
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if UserService.get_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if UserService.get_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return UserService.create(db, user_data)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user(current_user: User = Depends(get_current_user_dependency)):
    return current_user

# Dependency to get current user from token
def get_current_user_dependency(db: Session = Depends(get_db), token: str = Depends(OAuth2PasswordRequestForm)):
    # This is a simplified version - in production use proper JWT validation
    pass
