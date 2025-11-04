from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import verify_token, extract_user_info
from app.schemas.token import UserData


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserData:
    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_info = extract_user_info(payload)

    if not user_info.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    return user_info


def require_role(*allowed_roles: str):
    async def role_checker(user_data: UserData = Depends(get_current_user)) -> UserData:
        if user_data.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {', '.join(allowed_roles)}",
            )
        return user_data

    return role_checker


async def get_current_admin(
    user_data: UserData = Depends(require_role("admin")),
) -> UserData:
    return user_data
