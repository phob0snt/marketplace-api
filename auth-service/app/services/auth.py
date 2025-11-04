from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.auth import AuthORM
from app.schemas.auth import AccountCreate, AccountLogin, AccountResponse, RefreshRequest
from app.schemas.token import UserData, TokenPair
import app.repository.account as account_repo
from app.services.redis_client import redis_client
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)

def authenticate_user(login_data: AccountLogin, db: Session):
    user = account_repo.get_account_by_login(login_data.login, db)

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password")

    return AccountResponse(
        id=user.id,
        login=user.login,
        token_pair=create_token_pair(user)
    )

def refresh_token_pair(refresh_token: RefreshRequest, db: Session) -> TokenPair:
    user_data = verify_token(refresh_token.refresh_token, "refresh")

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token")
    
    user = account_repo.get_account_by_login(user_data.login, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return create_token_pair(user)
    

def create_token_pair(user: AuthORM) -> TokenPair:
    access_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_expires = timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))

    token_data = UserData(
        login=user.login,
        user_id=user.id,
        role=user.role
    )

    access_token = create_access_token(
        data=token_data,
        expires_delta=access_expires
    )

    refresh_token = create_refresh_token(
        data=token_data,
        expires_delta=refresh_expires
    )

    return TokenPair(access_token=access_token, refresh_token=refresh_token)

def register_user(
    register_data: AccountCreate,
    db: Session
):
    user = account_repo.get_account_by_login(register_data.login, db)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login is already used")

    return account_repo.create_account(register_data, db)

def register_user_with_login(
    register_data: AccountCreate,
    db: Session
) -> AccountResponse:
    
    user = register_user(register_data, db)

    return AccountResponse(
        id=user.id,
        login=user.login,
        token_pair=create_token_pair(user)
    )

def logout_user(token: str) -> bool:
    payload = verify_token(token, "access")
    
    if payload is None:
        return False
    
    exp_datetime = datetime.fromtimestamp(payload.exp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    ttl_seconds = int((exp_datetime - now).total_seconds())
    
    if ttl_seconds > 0:
        success = redis_client.add_to_blacklist(token, ttl_seconds)
        
        if not success:
            return False
    
    return True