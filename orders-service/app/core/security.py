import os
from typing import Literal

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY не найден в переменных окружения")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def verify_token(token: str, type: Literal["access", "refresh"]) -> dict:
    """Проверяет JWT токен и возвращает логин и роль пользователя"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (payload.get("type") != type):
            return None
        return payload
    except JWTError:
        return None