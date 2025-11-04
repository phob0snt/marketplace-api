from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base

import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
