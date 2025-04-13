from pydantic import BaseModel, EmailStr
from app.schemas.role import RoleOut

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # No lo guardamos así, solo para entrada

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleOut  # 👈 incluir rol

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRoleUpdate(BaseModel):
    role_id: int 