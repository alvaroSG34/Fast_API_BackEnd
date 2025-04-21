from pydantic import BaseModel
from typing import Optional
class ProveedorBase(BaseModel):
    nombre_empresa: str
    contacto_nombre: str
    email: str
    telefono: str
    direccion: str | None = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre_empresa: Optional[str] = None
    contacto_nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorOut(ProveedorBase):
    id: int

    class Config:
        orm_mode = True
