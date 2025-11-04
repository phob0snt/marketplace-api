import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/orders")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    from app.models.base import Base
    
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()