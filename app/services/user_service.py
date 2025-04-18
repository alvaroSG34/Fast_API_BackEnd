from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password
from app.models.role import Role

def create_user(db: Session, user: UserCreate) -> User:
    # Buscar el rol por defecto
    default_role = db.query(Role).filter(Role.name == "cliente").first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Rol por defecto no encontrado")

    hashed_pw = hash_password(user.password)
    new_user = User(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email,
        telefono=user.telefono,
        hashed_password=hashed_pw,
        fecha_registro=datetime.utcnow(),
        role_id=default_role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
