from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductResponse, ProductUpdateQuantity
from app.services import product as product_service
from app.schemas.token import UserData
from app.core.auth import get_current_admin
from app.db.session import get_db

router = APIRouter(tags=["products"])


@router.post("/products", response_model=ProductResponse)
def create_product(
    data: ProductCreate,
    _: UserData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return product_service.create_product(data, db)


@router.patch("/products/{product_id}", response_model=ProductResponse)
def change_stock_quantity(
    data: ProductUpdateQuantity,
    _: UserData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product = product_service.change_stock_quantity(data, "set", db)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(product_id, db)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


@router.get("/products", response_model=List[ProductResponse])
def list_products(offset: int, limit: int, db: Session = Depends(get_db)):
    return product_service.list_products(offset, limit, db)


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    _: UserData = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    result = product_service.delete_product(product_id, db)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return {"detail": "Product deleted successfully"}
