from datetime import datetime
from app.core import settings
from app.schemas.token import TokenPayload, UserData
from app.services.redis_client import redis_client

from jose import JWTError, jwt

def verify_token(token: str) -> TokenPayload | None:
    """Проверяет JWT токен и возвращает payload"""
    try:
        if redis_client.is_blacklisted(token):
            print(f"Token is blacklisted")
            return None
        
        payload_dict = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        payload = TokenPayload(**payload_dict)

        if (payload.type != "access"):
            return None
        
        if payload.exp and datetime.fromtimestamp(payload.exp) < datetime.now():
            return None
        
        return payload
    
    except JWTError:
        return None
    
def extract_user_info(payload: TokenPayload) -> UserData:
    return UserData(
        user_id=payload.user_id,
        login=payload.login,
        role=payload.role
    )