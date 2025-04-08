from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse

# Esquema para crear un CartItem
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

# Esquema para actualizar un CartItem
class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)

# Esquema para respuesta de CartItem
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

# Esquema para respuesta de Carrito
class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[CartItemResponse] = []
    total: float = 0
    
    class Config:
        from_attributes = True

# Esquema para aplicar descuento
class ApplyDiscount(BaseModel):
    discount_code: str
    cart_id: int 