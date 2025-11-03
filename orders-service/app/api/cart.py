from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cart import CartCreate, CartResponse
from app.services import cart as cart_service
from app.db.session import get_db

router = APIRouter(tags=["carts"])

@router.post("/cart", response_model=CartResponse)
def create_cart(db: Session = Depends(get_db)):
    data = CartCreate(user_id=1)
    cart = cart_service.create_cart_for_user(data, db)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create cart"
        )
    
    return cart

@router.get("/cart", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db)):
    cart = cart_service.get_cart_by_user_id(1, db)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    return cart

@router.post("/cart/clear")
def clear_cart(db: Session = Depends(get_db)):
    result = cart_service.clear_cart_for_user(1, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to clear cart"
        )
    
    return {"detail": "Cart cleared successfully"}