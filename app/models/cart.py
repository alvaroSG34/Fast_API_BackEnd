import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CarritoCompra(Base):
    __tablename__ = "carritocompra"

    id_carrito = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("users.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    estado = Column(String, default="activo")  # "activo", "guardado", "procesado", "abandonado"
    subtotal = Column(Float, default=0.0)

    # Relaciones
    usuario = relationship("User", backref="carritos")
    items = relationship("DetalleCarrito", back_populates="carrito", cascade="all, delete-orphan") 