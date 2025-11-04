from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.order import OrderResponse, OrderStatusResponse, OrderUpdateStatus
from app.schemas.token import UserData
from app.models.order import OrderStatus
from app.services import order as order_service
from app.core.auth import get_current_admin, get_current_user
from app.db.session import get_db

router = APIRouter(tags=["orders"])


@router.post("/orders", response_model=OrderResponse)
def create_order(
    user: UserData = Depends(get_current_user), db: Session = Depends(get_db)
):
    order = order_service.create_order(user.user_id, db)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create order"
        )

    return order


@router.get("/orders", response_model=List[OrderResponse])
def list_orders(
    user: UserData = Depends(get_current_user), db: Session = Depends(get_db)
):
    return order_service.get_user_orders(user.user_id, db)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    user: UserData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = order_service.get_order_by_id_and_user(order_id, user.user_id, db)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return order


@router.post("/orders/{order_id}/cancel", response_model=OrderStatusResponse)
def cancel_order(
    order_id: int,
    user: UserData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = OrderUpdateStatus(
        order_id=order_id, user_id=user.user_id, new_status=OrderStatus.CANCELED
    )

    order = order_service.change_order_status(data, db)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to cancel order"
        )

    return order


@router.post("/orders/{order_id}/complete", response_model=OrderStatusResponse)
def complete_order(
    order_id: int,
    user: UserData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    data = OrderUpdateStatus(
        order_id=order_id, user_id=user.user_id, new_status=OrderStatus.COMPLETED
    )

    order = order_service.change_order_status(data, db)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to complete order"
        )

    return order
