from pydantic import BaseModel
from typing import Optional
class ProductBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio_compra: float
    precio_venta: float
    imagen: str | None = None
    estado: bool = True
    id_categoria: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    imagen: Optional[str] = None
    estado: Optional[bool] = None
    id_categoria: Optional[int] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
