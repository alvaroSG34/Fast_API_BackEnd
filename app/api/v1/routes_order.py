from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user, get_current_user_with_permissions
from app.services import order as order_service
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate, OrderFilter

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear una nueva orden.
    Si user_id no coincide con el usuario autenticado, se requieren permisos de administrador.
    """
    # Verificar si el usuario tiene permisos para crear órdenes para otros usuarios
    if order.user_id != current_user.id:
        # Verificar que sea administrador
        admin_user = get_current_user_with_permissions(["admin"])
        current_user = admin_user(current_user)
    
    return order_service.create_order(db=db, order=order)

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """Obtener todas las órdenes. Solo administradores pueden ver todas las órdenes."""
    orders = order_service.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener las órdenes del usuario autenticado."""
    # Crear filtro con el usuario actual
    filters = OrderFilter(user_id=current_user.id)
    orders = order_service.filter_orders(db, filters=filters, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener una orden específica.
    El usuario solo puede ver sus propias órdenes, a menos que sea administrador.
    """
    db_order = order_service.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    
    # Verificar permisos
    if db_order.user_id != current_user.id:
        # Verificar que sea administrador
        admin_user = get_current_user_with_permissions(["admin"])
        current_user = admin_user(current_user)
    
    return db_order

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Actualizar el estado de una orden.
    Solo administradores pueden cambiar el estado de las órdenes.
    """
    db_order = order_service.update_order_status(db, order_id=order_id, status_update=status_update)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return db_order

@router.post("/filter", response_model=List[OrderResponse])
def filter_orders(
    filters: OrderFilter,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Filtrar órdenes según varios criterios.
    Solo administradores pueden usar esta funcionalidad.
    """
    orders = order_service.filter_orders(db, filters=filters, skip=skip, limit=limit)
    return orders

@router.get("/stats/overview", response_model=Dict[str, Any])
def get_orders_stats(
    user_id: int = None,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener estadísticas de órdenes.
    Si se solicitan estadísticas de otro usuario, se requieren permisos de administrador.
    """
    # Verificar permisos si se solicitan estadísticas de otro usuario
    if user_id is not None and user_id != current_user.id:
        # Verificar que sea administrador
        admin_user = get_current_user_with_permissions(["admin"])
        current_user = admin_user(current_user)
    
    stats = order_service.get_order_stats(db, user_id=user_id, days=days)
    return stats 