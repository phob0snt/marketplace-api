from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int


class ProductCreate(ProductBase):
    stock_quantity: int


class ProductDelete(ProductBase):
    id: int


class ProductUpdateQuantity(BaseModel):
    id: int
    quantity: int


class ProductResponse(ProductBase):
    id: int
    stock_quantity: int

    class Config:
        from_attributes = True
