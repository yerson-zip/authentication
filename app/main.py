from fastapi import FastAPI, Depends

from app.auth.dependencies import get_current_user
from app.auth.router import router as router_auth
from app.users.router import router as router_user

app = FastAPI()

app.include_router(router_auth)

app.include_router(router_user, dependencies=[Depends(get_current_user)])


