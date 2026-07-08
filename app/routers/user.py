from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.user import(
    UserCreate,
    UserResponse
)

from app.services.user import create_user

router = APIRouter(
    prefix= "/users",
    tags= ["Users"]
)

@router.post(
    "/register",
    response_model= UserResponse,
    status_code=201
)

def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail= str(e)
)