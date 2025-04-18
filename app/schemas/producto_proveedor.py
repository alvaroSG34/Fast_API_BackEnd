from pydantic import BaseModel
from datetime import datetime

from app.schemas.product import ProductOut
from app.schemas.proveedor import ProveedorOut

class ProductoProveedorBase(BaseModel):
    id_producto: int
    id_proveedor: int
    precio_compra: float
    codigo_proveedor: str | None = None
    es_proveedor_principal: bool = False
    ultima_compra: datetime | None = None
    producto: ProductOut
    proveedor: ProveedorOut

class ProductoProveedorCreate(ProductoProveedorBase):
    pass

class ProductoProveedorOut(ProductoProveedorBase):
    id: int

    class Config:
        orm_mode = True
