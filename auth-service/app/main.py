from fastapi import FastAPI

from app.api import auth

app = FastAPI(title="Marketplace API Auth Service", version="1.0.0")

app.include_router(auth.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Orders Service!"}