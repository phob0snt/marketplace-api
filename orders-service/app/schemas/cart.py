from typing import List, Optional
from pydantic import BaseModel

from .cart_item import CartItemCreate, CartItemResponse

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    items: Optional[List[CartItemCreate]] = []

class CartResponse(CartBase):
    id: int
    items: List[CartItemResponse] = []

    class Config:
        orm_mode = True