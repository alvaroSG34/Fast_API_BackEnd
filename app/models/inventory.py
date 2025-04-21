from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

def utc_now():
    return datetime.now(timezone.utc)

class Inventory(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    stock_actual = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    producto = relationship("Product", back_populates="inventario")
