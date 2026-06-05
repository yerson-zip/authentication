from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core import config
from app.auth.schemas import LoginRequest
from app.users.service import get_user_by_email
from app.core.security import hash_validate

def create_access_token(data:dict)->str:
    payload={
        "sub":str(data["id"]),
        "rol":data["rol"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=int(config.time_jwt))
    }

    return jwt.encode(payload, config.secret_key, algorithm=config.algorithm)

def verification_token(token:str)->dict |None:
    try:
        payload = jwt.decode(token, config.secret_key,algorithms=config.algorithm)
        return payload
    except JWTError:
        return None


def login_service(db:Session,user_login:LoginRequest)->str:
    user = get_user_by_email(db,user_login.email)

    if user is None or not hash_validate(user.password,user_login.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(data={
        "id":user.id,
        "rol":user.rol
    })

    return token


