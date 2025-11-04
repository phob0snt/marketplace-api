from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: int
    login: str
    role: str
    type: str
    exp: int


class UserData(BaseModel):
    user_id: int
    login: str
    role: str
