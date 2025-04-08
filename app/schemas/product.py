from pydantic import BaseModel, Field
from typing import Optional

# Esquema base para producto
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = None

# Esquema para crear productos
class ProductCreate(ProductBase):
    pass

# Esquema para actualizar productos
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

# Esquema para respuesta de productos
class ProductResponse(ProductBase):
    id: int
    is_active: bool = True
    
    class Config:
        from_attributes = True

# Esquema para búsqueda o filtrado de productos
class ProductFilter(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None 