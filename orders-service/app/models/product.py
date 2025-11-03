from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)