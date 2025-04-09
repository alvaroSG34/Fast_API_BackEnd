from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse
from app.models.order import OrderStatus

# Esquema para crear un OrderItem
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

# Esquema para respuesta de OrderItem
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

# Esquema para crear Order
class OrderCreate(BaseModel):
    user_id: int
    total_amount: float = Field(..., gt=0)
    items: List[OrderItemCreate]

# Esquema para respuesta de Order
class OrderResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str
    total_amount: float
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

# Esquema para actualizar estado de Order
class OrderStatusUpdate(BaseModel):
    status: str = Field(..., description="Estado de la orden")

    class Config:
        use_enum_values = True

# Esquema para filtrar órdenes
class OrderFilter(BaseModel):
    user_id: Optional[int] = None
    status: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None 