from pydantic import BaseModel, Field

class AccountCreate(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    password_confirm: str = Field(..., min_length=6, max_length=100)

class AccountLogin(BaseModel):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class AccountResponse(BaseModel):
    id: int
    login: str
    token_pair: TokenPair

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    login: str

    class Config:
        orm_mode = True