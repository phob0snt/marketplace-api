from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cart_item import CartItemCreate, CartItemResponse
from app.services import cart_item as cart_item_service
from app.db.session import get_db

router = APIRouter(tags=["cart_items"])

@router.post("/cart/add", response_model=CartItemResponse)
def create_cart_item(data: CartItemCreate, db: Session = Depends(get_db)):
    item = cart_item_service.create_cart_item(data, 1, db)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to add item to cart"
        )
    
    return item

@router.get("/cart/items", response_model=List[CartItemResponse])
def list_cart_items(db: Session = Depends(get_db)):
    return cart_item_service.list_cart_items(1, db)

@router.patch("/cart/items/{cart_item_id}/change_quantity", response_model=CartItemResponse)
def change_cart_item_quantity(cart_item_id: int, new_quantity: int, db: Session):
    item = cart_item_service.change_cart_item_quantity(cart_item_id, new_quantity, 1, db)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to change cart item quantity"
        )
    
    return item

@router.get("/cart/items/{cart_item_id}", response_model=CartItemResponse)
def get_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    item = cart_item_service.get_cart_item_by_id(cart_item_id, 1, db)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    return item

@router.delete("/cart/items/{cart_item_id}")
def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    result = cart_item_service.delete_cart_item(cart_item_id, 1, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    return {"detail": "Cart item deleted successfully"}