import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=False, index=True)
    apellido = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String, unique=False, index=True)
    hashed_password = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.UTC)  # 👈 Cambiado a String para almacenar la fecha como texto
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)  
    role = relationship("Role")  # 👈 Relación a objeto Role
