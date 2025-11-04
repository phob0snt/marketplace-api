from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cart_item import CartItemCreate, CartItemResponse, CartItemUpdateQuantity
from app.repository import cart as cart_repo
from app.repository import cart_item as cart_item_repo
from app.services import product as product_service

def create_cart_item(
        data: CartItemCreate,
        user_id: int,
        db: Session
) -> CartItemResponse | None:
    
    cart_item = cart_item_repo.create(data, user_id, db)

    if not cart_item:
        return None
    
    product = product_service.get_product_by_id(data.product_id, db)

    if not product:
        return None

    new_cart_item = CartItemResponse(
        id=cart_item.id,
        product=product,
        quantity=data.quantity
    )

    return new_cart_item

def list_cart_items(
        user_id: int,
        db: Session
) -> list[CartItemResponse]:
    cart_items = cart_item_repo.list_cart_items(user_id, db)

    cart_item_responses = []

    for item in cart_items:
        product = product_service.get_product_by_id(item.product_id, db)
        if not product:
            continue

        cart_item_response = CartItemResponse(
            id=item.id,
            product=product,
            quantity=item.quantity
        )
        cart_item_responses.append(cart_item_response)

    return cart_item_responses

def change_cart_item_quantity(
        cart_item_id: int,
        data: CartItemUpdateQuantity,
        user_id: int,
        db: Session
) -> CartItemResponse | None:
    cart_item = cart_item_repo.get_cart_item_by_id(cart_item_id, db)

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    cart = cart_repo.get_cart_by_user_id(user_id, db)

    if cart_item.cart_id != cart.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: this cart item not belongs to the user"
        )
    
    updated_cart_item = cart_item_repo.change_quantity(cart_item_id, data, db)

    product = product_service.get_product_by_id(cart_item.product_id, db)

    if not product:
        return None

    updated_cart_item = CartItemResponse(
        id=cart_item.id,
        product=product,
        quantity=cart_item.quantity
    )

    return updated_cart_item

def get_cart_item_by_id(cart_item_id: int, user_id: int, db: Session) -> CartItemResponse | None:
    cart_item = cart_item_repo.get_cart_item_by_id(cart_item_id, db)
    if not cart_item:
        return None
    
    user_cart = cart_repo.get_cart_by_user_id(user_id, db)

    if cart_item.cart_id != user_cart.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: this cart item not belongs to the user"
        )
    
    product = product_service.get_product_by_id(cart_item.product_id, db)
    if not product:
        return None
    
    return CartItemResponse(
        id=cart_item.id,
        product=product,
        quantity=cart_item.quantity
    )

def delete_cart_item(cart_item_id: int, user_id: int, db: Session) -> bool:
    user_cart = cart_repo.get_cart_by_user_id(user_id, db)
    cart_item = cart_item_repo.get_cart_item_by_id(cart_item_id, db)

    if not cart_item:
        return False
    
    if cart_item.cart_id != user_cart.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: this cart item not belongs to the user"
        )
    
    return cart_item_repo.delete(cart_item_id, db)