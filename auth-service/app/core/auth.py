from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.token import UserData
from app.services.redis_client import redis_client
from .security import verify_token, extract_user_info

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserData:
    token = credentials.credentials

    if redis_client.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )

    payload = verify_token(token, "access")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_info = extract_user_info(payload)

    if not user_info.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    return user_info