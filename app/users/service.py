from dns import exception
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.users.models import User
from app.auth.schemas import RegisterRequest
from app.core.security import password_hash

error_404 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST
    ,detail="Credenciales invalidas")

def create_user(user_request:RegisterRequest, db:Session):
    user_db = User(
        **user_request.model_dump(exclude={"password"}),
        password=password_hash(user_request.password))
    try:
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email existente")

def get_user_by_email(db:Session, email:str):
    user = db.query(User).filter(User.email==email).first()

    if user is None:
        raise error_404

    return user


def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise error_404

    return user
