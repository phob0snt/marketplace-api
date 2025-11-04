from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class AuthORM(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="user", nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
