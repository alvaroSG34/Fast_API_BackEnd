from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class MetodoPago(str, Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"
    transferencia = "transferencia"
    otro = "otro"

class DetalleVentaCreate(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    descuento: float = 0.0
    subtotal: float

class VentaCreate(BaseModel):
    id_usuario: int
    fecha_venta: datetime
    subtotal: float
    descuento: float
    total: float
    metodo_pago: MetodoPago
    detalles: List[DetalleVentaCreate]

class DetalleVentaOut(BaseModel):
    id_producto: int
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class ItemFactura(BaseModel):
    id_producto: int
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

class FacturaVenta(BaseModel):
    numero_factura: str
    cliente: str
    fecha_venta: datetime
    metodo_pago: str
    estado: str
    subtotal: float
    descuento: float
    total: float
    items: List[ItemFactura]    

class VentaResumen(BaseModel):
    id_venta: int
    numero_factura: str
    fecha_venta: datetime
    total: float
    metodo_pago: str
    estado: str
    cliente: Optional[str]

class VentaConDetalle(VentaResumen):
    detalles: List[DetalleVentaOut]    

    class Config:
        orm_mode = True
     
        

