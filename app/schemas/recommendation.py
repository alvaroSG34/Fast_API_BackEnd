from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductResponse

# Esquema para respuesta de recomendación de producto
class ProductRecommendationResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    score: float
    created_at: datetime
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

# Esquema para crear asociación de productos
class ProductAssociationCreate(BaseModel):
    product_id: int
    associated_product_id: int
    strength: float = Field(..., ge=0, le=1)

# Esquema para respuesta de asociación de productos
class ProductAssociationResponse(BaseModel):
    id: int
    product_id: int
    associated_product_id: int
    strength: float
    product: Optional[ProductResponse] = None
    associated_product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

# Esquema para parámetros de recomendación
class RecommendationParams(BaseModel):
    limit: int = Field(5, ge=1, le=20, description="Número máximo de recomendaciones")
    min_score: float = Field(0.0, ge=0, le=1, description="Puntuación mínima")
    include_viewed: bool = Field(False, description="Incluir recomendaciones ya vistas") 