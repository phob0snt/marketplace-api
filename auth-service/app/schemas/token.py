from pydantic import BaseModel


class UserData(BaseModel):
    login: str
    user_id: int
    role: str

class TokenPayload(UserData):
    exp: int
    type: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
