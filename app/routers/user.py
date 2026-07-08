from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.security import get_current_user

from app.schemas.user import(
    UserCreate,
    UserResponse
)
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import (
    Token
)

from app.services.auth import(
    authenticate_user,
    generate_token
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
    
@router.post(
    "/login",
    response_model= Token
)

def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        credentials.username,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code= 401,
            detail= "Inavlid email or password"
        )
    
    access_token = generate_token(user)

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserResponse
)

def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    return current_user