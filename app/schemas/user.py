from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.role import RoleOut

# ✅ Para crear usuario (registro)
class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    password: str  # No lo guardamos así, solo para entrada

# ✅ Para devolver usuario completo
class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str
    fecha_registro: datetime
    role: Optional[RoleOut]

    class Config:
        orm_mode = True

# ✅ Para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ✅ Actualización de rol
class UserRoleUpdate(BaseModel):
    role_id: int
