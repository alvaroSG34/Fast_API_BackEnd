from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.services.auth import verify_password, create_access_token
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()
    if not db_user or not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token(data={
    "sub": str(db_user.id),
    "role": db_user.role.name  # 👈 Agregamos el rol al payload del token
})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")

    # Crear el usuario con rol cliente por defecto
    return create_user(db, user)
