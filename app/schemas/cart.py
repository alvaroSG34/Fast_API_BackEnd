from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.cart_item import CartItemOut

class CartBase(BaseModel):
    id_usuario: int
    estado: Optional[str] = "activo"
    subtotal: Optional[float] = 0.0

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    estado: Optional[str] = None
    subtotal: Optional[float] = None

class CartOut(CartBase):
    id_carrito: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True

class CartWithItems(CartOut):
    items: List[CartItemOut] = []

    class Config:
        orm_mode = True 