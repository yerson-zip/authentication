from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    id: int
    email:str
    full_name:str
    rol:str

    model_config = ConfigDict(from_attributes=True)