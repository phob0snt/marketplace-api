from pydantic import BaseModel

from .cart import CartResponse
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    cart: CartResponse
    user_id: int


class OrderResponse(OrderCreate):
    id: int
    status: str

    class Config:
        orm_mode = True


class OrderStatusResponse(BaseModel):
    order_id: int
    status: str

    class Config:
        orm_mode = True


class OrderUpdateStatus(BaseModel):
    order_id: int
    user_id: int
    new_status: OrderStatus
