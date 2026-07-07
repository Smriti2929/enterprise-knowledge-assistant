from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import Base, engine

from app.models import User

app = FastAPI(title= "Enterprise Knowledge Assistant")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Enterprise Knowledge Assistant API"}

@app.get("/health")
def health_check():
    #The with statement automatically closes the connection afterward.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "Databse Connected Successfully"}    