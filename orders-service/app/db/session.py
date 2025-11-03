import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL", f"postgresql://postgres:postgres@localhost:5432/orders")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    from app.models.base import Base
    from app.models.product import Product
    from app.models.cart_item import CartItem
    from app.models.cart import Cart
    
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()