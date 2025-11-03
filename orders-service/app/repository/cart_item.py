from app.schemas.cart_item import CartItemCreate
from app.models.cart_item import CartItem
from app.models.cart import Cart

from sqlalchemy.orm import Session


def create(data: CartItemCreate, user_id: int, db: Session) -> CartItem | None:
    cart_id = db.query(Cart).filter(Cart.user_id == user_id).first().id
    if not cart_id:
        return None
    
    new_cart_item = CartItem(
        cart_id=cart_id,
        product_id=data.product_id,
        quantity=data.quantity
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item    

def delete(cart_item_id: int, db: Session) -> bool:
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        return False

    db.delete(cart_item)
    db.commit()

    return True

def list_cart_items(user_id: int, db: Session) -> list[CartItem]:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        return []
    
    return db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

def get_cart_item_by_id(cart_item_id: int, db: Session) -> CartItem | None:
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        return None
    
    return cart_item

def change_quantity(cart_item_id: int, new_quantity: int, db: Session) -> CartItem | None:
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        return None

    cart_item.quantity = new_quantity
    db.commit()
    db.refresh(cart_item)

    return cart_item