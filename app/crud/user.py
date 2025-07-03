from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(and_(User.id == user_id, User.is_active == True)).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(and_(User.username == username, User.is_active == True)).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(and_(User.email == email, User.is_active == True)).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user