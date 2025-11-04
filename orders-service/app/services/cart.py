from sqlalchemy.orm import Session

from app.schemas.cart import CartCreate, CartResponse
from app.schemas.cart_item import CartItemResponse
from app.repository import cart as cart_repo


def create_cart_for_user(data: CartCreate, db: Session) -> CartResponse:
    cart = cart_repo.create(data, db)

    new_cart = CartResponse(
        user_id=cart.user_id,
        id=cart.id,
        items=[],
    )

    return new_cart


def get_cart_by_user_id(user_id: int, db: Session) -> CartResponse | None:
    cart = cart_repo.get_cart_by_user_id(user_id, db)

    if not cart:
        return None

    cart_response = CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=[CartItemResponse.model_validate(item) for item in cart.items],
    )

    return cart_response


def clear_cart_for_user(user_id: int, db: Session) -> bool:
    cart = cart_repo.get_cart_by_user_id(user_id, db)
    return cart_repo.clear_cart(cart.id, db)
