from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String, nullable=False)
    contacto_nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    productos = relationship("ProductoProveedor", back_populates="proveedor")
