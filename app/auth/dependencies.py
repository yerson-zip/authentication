from fastapi import Request, HTTPException, status, Depends
from pygments.lexers import verification
from sqlalchemy.orm import Session

from app.auth.service import verification_token
from app.core.database import get_db
from app.users.models import User
from app.users.service import get_user_by_id

def get_token(request:Request)->str:
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return authorization.split(" ")[1]


def get_current_user(db:Session=Depends(get_db), token:str= Depends(get_token))->User:
    payload = verification_token(token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    sub = payload["sub"]

    user = get_user_by_id(db,int(sub))

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    return user

def require_role(required_role:str):
    def checker(user:User=Depends(get_current_user)):
        if user.rol != required_role:
            raise HTTPException(status_code=403, detail="Sin permisos")
        return user
    return checker




