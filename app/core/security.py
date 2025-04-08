from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

# Configuración de JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Función para verificar el token y obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificar el token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Verificar que el usuario está activo
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    # Aquí podrías verificar si el usuario está activo
    # Por ejemplo: if not current_user.is_active: raise HTTPException(...)
    return current_user

# Verificar si el usuario tiene los permisos necesarios (función factory)
def get_current_user_with_permissions(required_roles: List[str]):
    async def _get_user_with_permissions(current_user: User = Depends(get_current_user)) -> User:
        # Aquí deberías implementar la lógica de verificación de roles
        # Por ejemplo, verificar en la base de datos si el usuario tiene alguno de los roles requeridos
        # Por ahora, asumimos que el usuario con ID 1 es admin
        if current_user.id == 1 or "admin" in required_roles:
            return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes suficientes permisos para esta acción"
        )
    return _get_user_with_permissions 