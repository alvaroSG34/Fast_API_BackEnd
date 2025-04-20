from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class DetalleVenta(Base):
    __tablename__ = "detalleventa"

    id_detalle_venta = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), nullable=False, default=0)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Product", back_populates="detalles_venta") 