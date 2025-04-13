from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password
from app.models.role import Role

def create_user(db: Session, user: UserCreate) -> User:
    # Buscar el rol por defecto (por ejemplo, "vendedor")
    default_role = db.query(Role).filter(Role.name == "cliente").first()
    if not default_role:
        raise HTTPException(status_code=500, detail="Rol por defecto no encontrado")

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role_id=default_role.id  # 👈 asignar el rol por defecto
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
