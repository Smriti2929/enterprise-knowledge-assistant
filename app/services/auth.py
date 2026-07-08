from jose import JWTError, jwt
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import(
    verify_password,
    create_access_token
)

from app.models.user import User
from app.schemas.auth import TokenData

def authenticate_user(
        db: Session,
        email: str,
        password: str
):
    #authenticate a user using email and password.

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None
    
    if not verify_password(
        password,
        user.hashed_password
    ):
        return None #if wrong
    
    return user#if correct return user

def generate_token(user: User):
    #generate JWT Token for authenticated user.

    access_token = create_access_token(
        data={
            "user_id": user.id
        }
    )

    return access_token

