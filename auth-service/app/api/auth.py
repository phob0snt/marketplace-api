from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountLogin, AccountResponse, RefreshRequest, TokenPair, UserResponse
from app.services import auth as auth_service
from app.core.security import get_current_user


router = APIRouter(tags=["auth"])

@router.post("/login", response_model=AccountResponse)
def login(login_data: AccountLogin, db: Session = Depends(get_db)):
    return auth_service.authenticate_user(login_data, db)

@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_token_pair(payload, db)

@router.post("/register", response_model=AccountResponse)
def register_user(register_data: AccountCreate, db: Session = Depends(get_db)):
    return auth_service.register_user_with_login(register_data, db)

@router.get("/me", response_model=UserResponse)
def get_current_user(user: AuthORM = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        login=user.login,
    )