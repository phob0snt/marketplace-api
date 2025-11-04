from datetime import datetime, timedelta
from typing import Literal, Optional
from pydantic import ValidationError
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas.token import UserData, TokenPayload
from app.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль против хеша"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Создает хеш пароля"""
    return pwd_context.hash(password)

def create_access_token(data: UserData, expires_delta: Optional[timedelta] = None):
    """Создает access токен"""
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)

    to_encode = TokenPayload(
        login=data.login,
        user_id=data.user_id,
        role=data.role,
        exp=int(expire.timestamp()),
        type="access"
    )

    encoded_jwt = jwt.encode(to_encode.model_dump(), settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: UserData, expires_delta: Optional[timedelta] = None):
    """Создает refresh токен"""
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=30)

    to_encode = TokenPayload(
        login=data.login,
        user_id=data.user_id,
        role=data.role,
        exp=int(expire.timestamp()),
        type="refresh"
    )

    encoded_jwt = jwt.encode(to_encode.model_dump(), settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, type: Literal["access", "refresh"]) -> TokenPayload | None:
    """Проверяет JWT токен и возвращает payload"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if (payload.get("type") != type):
            return None
        
        token_data = TokenPayload(**payload)

        if token_data.exp and datetime.fromtimestamp(token_data.exp) < datetime.now():
            return None

        return token_data
    
    except JWTError:
        return None
    except ValidationError:
        return None

def extract_user_info(payload: TokenPayload) -> UserData:
    return UserData(
        user_id=payload.user_id,
        login=payload.login,
        role=payload.role
    )