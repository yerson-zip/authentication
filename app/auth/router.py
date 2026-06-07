from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.core.database import get_db
from app.users.models import User
from app.users.service import create_user
from app.users.schemas import UserResponse
from app.auth.service import login_service, refrescar_tokens, logout_service

from app.auth.model import Base
from app.core.database import engine
from app.auth.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_request: RegisterRequest, db:Session=Depends(get_db)):
    return create_user(user_request, db)

@router.post("/login", response_model=TokenResponse)
def login_(user_login:LoginRequest, db:Session=Depends(get_db)):
    return login_service(db, user_login)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data:RefreshRequest, db:Session=Depends(get_db)):
    return  refrescar_tokens(data.refresh_token, db)

@router.post("/logout")
def logout(tokens:RefreshRequest,user=Depends(get_current_user), db:Session=Depends(get_db)):
    return logout_service(user.id,tokens.refresh_token, db)