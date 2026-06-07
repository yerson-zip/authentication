import secrets

import bcrypt
from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.auth.model import RefreshToken
from app.core import config
from app.auth.schemas import LoginRequest
from app.users.models import User
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


def login_service(db:Session,user_login:LoginRequest)->dict:
    user = get_user_by_email(db,user_login.email)

    if user is None or not hash_validate(user.password,user_login.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={
        "id":user.id,
        "rol":user.rol
    })

    refresh_token = create_refresh_token(user.id, db)


    return {
        "access_token":access_token,
        "refresh_token": refresh_token
    }


def create_refresh_token(user_id:int, db:Session)->str:

    token = secrets.token_hex(32)
    hashed = bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()

    db_token = RefreshToken(
        token= hashed,
        user_id=user_id,
        expires_at=datetime.now(timezone.utc)+ timedelta(days=int(config.days))
    )

    db.add(db_token)
    db.commit()

    return token

def refrescar_tokens(refresh_token:str, db:Session)->dict:
    tokens = (db.query(RefreshToken)
              .filter(RefreshToken.revoked==False)
              .all())
    token_find = None

    for t in tokens:
        if bcrypt.checkpw(refresh_token.encode(), t.token.encode()):
            token_find=t
            break

    if not token_find:
        raise HTTPException(status_code=401, detail="Refresh token invalido")

    if token_find.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token expirado")

    token_find.revoked = True
    db.commit()

    statement = select(User.rol).where(User.id==token_find.user_id)
    role = db.execute(statement).scalar()

    new_access_token = create_access_token(data={
        "id":token_find.user_id,
        "rol":role
    })
    new_refresh_token = create_refresh_token(token_find.user_id, db)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

def logout_service(user_id:int, refresh_token:str, db:Session):

    token_fin = db.query(RefreshToken).filter(RefreshToken.user_id==user_id, RefreshToken.revoked==False).all()

    for t in token_fin:
        if bcrypt.checkpw(refresh_token.encode('utf-8'),t.token.encode("utf-8")):
            t.revoked=True
            db.commit()


    raise HTTPException(status_code=401, detail="Falta de credenciales")


