from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import (
    UserResponse,
    UserCreate,
    UserRoleUpdate
)
from app.services.user_service import create_user
from app.models.user import User
from app.services.dependencies import get_current_user, get_current_user_with_permissions

router = APIRouter()

# Dependency para la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear nuevo usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")
    return create_user(db, user)

# Eliminar usuario por ID
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()

# Listar todos los usuarios (solo admins)
@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    return db.query(User).all()

# Obtener perfil del usuario autenticado
@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Actualizar el rol del usuario
@router.put("/{user_id}/role", status_code=status.HTTP_200_OK)
def update_user_role(user_id: int, data: UserRoleUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.role_id = data.role_id
    db.commit()
    return {"detail": "Rol actualizado correctamente"}
