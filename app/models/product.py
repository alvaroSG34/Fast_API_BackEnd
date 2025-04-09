from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True, index=True)
    
    # Relaciones
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete")
    order_items = relationship("OrderItem", back_populates="product") 