from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    stock_quantity: int

class ProductDelete(ProductBase):
    id: int

class ProductUpdate(BaseModel):
    id: int
    new_stock_quantity: int
    
class ProductResponse(ProductBase):
    id: int
    stock_quantity: int

    class Config:
        orm_mode = True