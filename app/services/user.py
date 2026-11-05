
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


# Register User
def register_user(user: UserCreate, db: Session):

    if db.query(User).filter(User.email == user.email).first():
        raise ValueError("Email already exists")
        

    new_user = User(name=user.name,email=user.email,hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login User
def authenticate_user(email: str, password: str, db: Session):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    return user
