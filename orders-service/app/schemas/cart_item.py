from pydantic import BaseModel
from .product import ProductResponse

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(BaseModel):
    id: int
    quantity: int
    product: ProductResponse

    class Config:
        orm_mode = True