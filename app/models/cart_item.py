from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class DetalleCarrito(Base):
    __tablename__ = "detallecarrito"

    id_detalle_carrito = Column(Integer, primary_key=True, index=True)
    id_carrito = Column(Integer, ForeignKey("carritocompra.id_carrito"), nullable=False)
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    descuento = Column(Float, default=0.0)
    subtotal = Column(Float, nullable=False)

    # Relaciones
    carrito = relationship("CarritoCompra", back_populates="items")
    producto = relationship("Product") 