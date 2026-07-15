from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from app.schemas.auth import TokenData
from passlib.context import CryptContext

from app.core.config import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

#Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated= "auto"
)

oauth2_scheme= OAuth2PasswordBearer(
    tokenUrl= "/users/login"
)

def hash_password(password: str) -> str:
    #Hash the pw and then store

    return pwd_context.hash(password)

def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    #comapre its plain/ hash password.
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    #create JWT acess token

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta( #now() is Constraint
        minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token: str):

    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms= [settings.ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(
            user_id= user_id
        )

    except JWTError:
        raise credentials_exception

    return token_data    

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db : Session = Depends(get_db)
):
    token_data = verify_access_token(token)

    user = (
        db.query(User)
        .filter(User.id == token_data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user