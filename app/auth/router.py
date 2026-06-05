from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterRequest, LoginRequest
from app.core.database import get_db
from app.users.service import create_user
from app.users.schemas import UserResponse
from app.auth.service import login_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_request: RegisterRequest, db:Session=Depends(get_db)):
    return create_user(user_request, db)

@router.post("/login")
def login_(user_login:LoginRequest, db:Session=Depends(get_db)):
    return login_service(db, user_login)
