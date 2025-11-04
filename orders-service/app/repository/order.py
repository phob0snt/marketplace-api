from typing import List
from app.schemas.order import OrderCreate, OrderUpdateStatus
from app.models.order import Order
from app.models.order_item import OrderItem

from sqlalchemy.orm import Session


def create(data: OrderCreate, db: Session) -> Order:
    total_price = sum(item.product.price * item.quantity for item in data.cart.items)

    order = Order(user_id=data.user_id, total_price=total_price)

    db.add(order)
    db.flush()

    for item in data.cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price,
            subtotal=item.product.price * item.quantity,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    return order


def list_orders_by_user_id(user_id: int, db: Session) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id_and_user_id(
    order_id: int, user_id: int, db: Session
) -> Order | None:
    return (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    )


def change_status(data: OrderUpdateStatus, db: Session) -> Order:
    order = db.query(Order).filter(Order.id == data.order_id).first()
    order.status = data.new_status

    db.commit()
    db.refresh(order)

    return order
