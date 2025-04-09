from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ProductRecommendation(Base):
    __tablename__ = "product_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    score = Column(Float, nullable=False, default=0.0)  # Puntuación de relevancia
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_viewed = Column(Boolean, default=False)  # Si el usuario ha visto la recomendación
    
    # Relaciones
    user = relationship("User")
    product = relationship("Product")

class ProductAssociation(Base):
    __tablename__ = "product_associations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    associated_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    strength = Column(Float, nullable=False, default=0.0)  # Fuerza de la asociación
    
    # Relaciones
    product = relationship("Product", foreign_keys=[product_id])
    associated_product = relationship("Product", foreign_keys=[associated_product_id]) 