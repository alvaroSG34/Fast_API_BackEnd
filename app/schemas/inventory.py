from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.product import ProductOut
class InventoryBase(BaseModel):
    id_producto: int
    stock_actual: int
    stock_minimo: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None

class InventoryOut(InventoryBase):
    id: int
    fecha_actualizacion: datetime
    producto: ProductOut  

    class Config:
        orm_mode = True
