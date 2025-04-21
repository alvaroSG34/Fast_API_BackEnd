from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class EstadoVenta(str, enum.Enum):
    pendiente = "pendiente"
    completada = "completada"
    cancelada = "cancelada"
    anulada = "anulada"

class MetodoPago(str, enum.Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"
    transferencia = "transferencia"
    otro = "otro"

class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_factura = Column(String, nullable=False)
    id_usuario = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_venta = Column(DateTime, nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    descuento = Column(DECIMAL(10, 2), nullable=False, default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    estado = Column(Enum(EstadoVenta), nullable=False)

    # Relaciones
    usuario = relationship("User", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan") 