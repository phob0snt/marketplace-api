from app.schemas.product import ProductCreate, ProductUpdateQuantity
from sqlalchemy.orm import Session
from app.models.product import Product

def create(data: ProductCreate, db: Session) -> Product:
    new_product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock_quantity=data.stock_quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def get_product_by_id(product_id: int, db: Session) -> Product | None:
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return None
    
    return product

def list_products(offset: int, limit: int, db: Session) -> list[Product]:
    return db.query(Product).offset(offset).limit(limit).all()

def update_product_stock(data: ProductUpdateQuantity, db: Session) -> Product | None:
    product = db.query(Product).filter(Product.id == data.id).first()

    if not product:
        return None

    product.stock_quantity = data.new_stock_quantity
    db.commit()
    db.refresh(product)

    return product

def delete_product(product_id: int, db: Session) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return False

    db.delete(product)
    db.commit()

    return True