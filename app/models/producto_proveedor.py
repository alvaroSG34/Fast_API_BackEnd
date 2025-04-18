from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ProductoProveedor(Base):
    __tablename__ = "producto_proveedor"

    id = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("products.id"), nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    precio_compra = Column(Float, nullable=False)
    codigo_proveedor = Column(String, nullable=True)
    es_proveedor_principal = Column(Boolean, default=False)
    ultima_compra = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Product", back_populates="proveedores")
    proveedor = relationship("Proveedor", back_populates="productos")
