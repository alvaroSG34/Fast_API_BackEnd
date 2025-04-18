from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Inventory(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    producto = relationship("Product", back_populates="inventario")
