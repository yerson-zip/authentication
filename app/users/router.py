from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user,require_role

from app.users.models import Base
from app.core.database import engine
from app.users.schemas import UserResponse
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/me", response_model=UserResponse)
def perfil(user=Depends(get_current_user)):
    return user

@router.get("/role")
def role_(user =Depends(require_role("user"))):
    return "Permisos validos"