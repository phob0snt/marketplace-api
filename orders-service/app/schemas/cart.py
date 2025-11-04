from typing import List
from pydantic import BaseModel

from .cart_item import CartItemResponse

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: int
    items: List[CartItemResponse] = []

    class Config:
        orm_mode = True