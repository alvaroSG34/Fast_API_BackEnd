from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    imagen = Column(String, nullable=True)
    estado = Column(Boolean, default=True)
    id_categoria = Column(Integer, ForeignKey("categories.id"), nullable=False)

    categoria = relationship("Category", backref="productos")
    inventario = relationship("Inventory", back_populates="producto", uselist=False)
    proveedores = relationship("ProductoProveedor", back_populates="producto")
    detalles_venta = relationship("DetalleVenta", back_populates="producto")
    detalles_carrito = relationship("DetalleCarrito", back_populates="producto")

