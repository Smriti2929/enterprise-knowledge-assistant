from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(
        db: Session,
        user: UserCreate
):
     # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email 
    ).first()



    if existing_user:
        raise ValueError(
            "Email already exists"
        )

    # Create new user
    new_user = User(
        name = user.name,
        email= user.email,
        hashed_password = user.password
    )

    #save info in db

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

