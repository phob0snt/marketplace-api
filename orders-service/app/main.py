from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.api.cart_item import router as cart_item_router
from app.api.order import router as order_router
from app.db.session import SessionLocal
from app.core.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {str(e)}")
    finally:
        db.close()

    yield


app = FastAPI(
    title="Marketplace API Orders Service", version="1.0.0", lifespan=lifespan
)

app.include_router(product_router)
app.include_router(cart_router)
app.include_router(cart_item_router)
app.include_router(order_router)


@app.get("/")
def get_root():
    return {"message": "Welcome to the Orders Service!"}
