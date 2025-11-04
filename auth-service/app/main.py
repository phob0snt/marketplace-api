from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.api import auth
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


app = FastAPI(title="Marketplace API Auth Service", version="1.0.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth Service!"}
