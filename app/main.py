from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import Base, engine

from app.models import User

from app.routers.user import router as user_router

from app.routers.documents import router as document_router

app = FastAPI(title= "Enterprise Knowledge Assistant")

# Base.metadata.create_all(bind=engine) # Creating database tables

#including routers
app.include_router(user_router)
app.include_router(document_router)

@app.get("/")
def root():
    return {"message": "Enterprise Knowledge Assistant API"}

@app.get("/health")
def health_check():
    #The with statement automatically closes the connection afterward.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "Databse Connected Successfully"}    