from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.schemas.cart import CartCreate


def create(data: CartCreate, db: Session) -> Cart:
    new_cart = Cart(
        user_id=data.user_id,
    )

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)

    return new_cart

def get_cart_by_user_id(user_id: int, db: Session) -> Cart | None:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return None
    
    return cart

def clear_cart(cart_id: int, db: Session) -> bool:
    cart = db.query(Cart).filter(Cart.id == cart_id).first()

    if not cart:
        return False

    cart.items.clear()
    db.commit()

    return True