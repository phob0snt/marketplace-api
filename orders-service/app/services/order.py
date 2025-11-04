from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .cart import get_cart_by_user_id
from .product import get_product_by_id, change_stock_quantity
from app.schemas.cart import CartResponse
from app.schemas.order import (
    OrderCreate,
    OrderResponse,
    OrderStatusResponse,
    OrderUpdateStatus,
)
from app.schemas.product import ProductResponse, ProductUpdateQuantity


def create_order(user_id: int, db: Session) -> OrderResponse:
    cart: CartResponse = get_cart_by_user_id(user_id, db)

    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )

    for cart_item in cart.items:
        product: ProductResponse = get_product_by_id(cart_item.product.id, db)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {cart_item.product.id} not found",
            )

        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product '{product.name}'. Available: {product.stock_quantity}, requested: {cart_item.quantity}",
            )

    from app.repository import order as order_repo

    data = OrderCreate(
        cart=cart,
        user_id=user_id,
    )

    order = order_repo.create(data, db)

    for cart_item in cart.items:
        product_update = ProductUpdateQuantity(
            id=cart_item.product.id, quantity=-cart_item.quantity
        )
        change_stock_quantity(product_update, "add", db)

    response = OrderResponse(
        cart=cart, id=order.id, user_id=order.user_id, status=order.status
    )

    return response


def get_user_orders(user_id: int, db: Session) -> list[OrderResponse]:
    from app.repository import order as order_repo

    orders = order_repo.list_orders_by_user_id(user_id, db)

    order_responses = []

    for order in orders:
        cart = get_cart_by_user_id(user_id, db)

        order_response = OrderResponse(
            id=order.id, user_id=order.user_id, cart=cart, status=order.status
        )
        order_responses.append(order_response)

    return order_responses


def get_order_by_id_and_user(
    order_id: int, user_id: int, db: Session
) -> OrderResponse | None:
    from app.repository import order as order_repo

    order = order_repo.get_order_by_id_and_user_id(order_id, user_id, db)

    if not order:
        return None

    cart = get_cart_by_user_id(user_id, db)

    order_response = OrderResponse(
        id=order.id, user_id=order.user_id, cart=cart, status=order.status
    )

    return order_response


def change_order_status(
    data: OrderUpdateStatus, db: Session
) -> OrderStatusResponse | None:
    from app.repository import order as order_repo

    order = order_repo.change_status(data, db)

    if not order:
        return None

    order_response = OrderStatusResponse(
        order_id=order.id,
        status=order.status,
    )

    return order_response
