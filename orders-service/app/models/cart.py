from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .base import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")