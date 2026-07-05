from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine

app = FastAPI(title= "Enterprise Knowledge Assistant")

@app.get("/")
def root():
    return {"message": "Enterprise Knowledge Assistant API"}

@app.get("/health")
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "Databse Connected Successfully"}    