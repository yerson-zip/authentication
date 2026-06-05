from pydantic import BaseModel,EmailStr, ConfigDict

class RegisterRequest(BaseModel):
    email:EmailStr
    full_name:str
    password:str
    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


