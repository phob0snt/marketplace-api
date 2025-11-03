from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.repository import product as product_repo

def create_product(data: ProductCreate, db: Session) -> ProductResponse:
    product = product_repo.create(data, db)
    
    new_product = ProductResponse(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    return new_product

def change_stock_quantity(data: ProductUpdate, db: Session) -> ProductResponse | None:
    product = product_repo.update_product_stock(data, db)

    if not product:
        return None

    updated_product = ProductResponse(
        name=product.name,
        id=product.id,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    return updated_product

def get_product_by_id(product_id: int, db: Session) -> ProductResponse | None:
    product = product_repo.get_product_by_id(product_id, db)

    if not product:
        return None

    product_response = ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity
    )

    return product_response

def list_products(offset: int, limit: int, db: Session) -> list[ProductResponse]:
    products = product_repo.list_products(offset, limit, db)

    product_responses = [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity
        )
        for product in products
    ]

    return product_responses

def delete_product(product_id: int, db: Session) -> bool:
    return product_repo.delete_product(product_id, db)