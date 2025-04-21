from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    id_carrito: int
    id_producto: int
    cantidad: int
    precio_unitario: Optional[float] = None
    descuento: Optional[float] = 0.0
    subtotal: Optional[float] = None

class CartItemCreate(BaseModel):
    id_carrito: int
    id_producto: int
    cantidad: int = 1
    descuento: Optional[float] = 0.0

class CartItemUpdate(BaseModel):
    cantidad: Optional[int] = None
    descuento: Optional[float] = None
    subtotal: Optional[float] = None

class CartItemOut(CartItemBase):
    id_detalle_carrito: int
    nombre_producto: Optional[str] = None
    imagen_producto: Optional[str] = None

    class Config:
        orm_mode = True 