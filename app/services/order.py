from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderFilter
from sqlalchemy import and_, or_, func, desc

def get_order(db: Session, order_id: int) -> Optional[Order]:
    """Obtener una orden por su ID."""
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    """Obtener todas las órdenes."""
    return db.query(Order).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def create_order(db: Session, order: OrderCreate) -> Order:
    """Crear una nueva orden."""
    # Crear la orden
    db_order = Order(
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=OrderStatus.PENDING.value
    )
    db.add(db_order)
    db.flush()  # Para obtener el ID asignado
    
    # Crear los items de la orden
    order_items = []
    for item in order.items:
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        order_items.append(order_item)
        
        # Actualizar stock del producto
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock >= item.quantity:
            product.stock -= item.quantity
        else:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {item.product_id}"
            )
    
    db.add_all(order_items)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status_update: OrderStatusUpdate) -> Optional[Order]:
    """Actualizar el estado de una orden."""
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    # Validar transición de estado
    current_status = db_order.status
    new_status = status_update.status
    
    # Por ejemplo: no se puede pasar de CANCELLED a PAID
    if current_status == OrderStatus.CANCELLED.value and new_status != OrderStatus.CANCELLED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cambiar el estado de una orden cancelada"
        )
    
    # Actualizar estado
    db_order.status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order

def filter_orders(db: Session, filters: OrderFilter, skip: int = 0, limit: int = 100) -> List[Order]:
    """Filtrar órdenes según varios criterios."""
    query = db.query(Order)
    
    # Aplicar filtros
    if filters.user_id:
        query = query.filter(Order.user_id == filters.user_id)
    
    if filters.status:
        query = query.filter(Order.status == filters.status)
    
    if filters.from_date:
        query = query.filter(Order.created_at >= filters.from_date)
    
    if filters.to_date:
        query = query.filter(Order.created_at <= filters.to_date)
    
    if filters.min_amount is not None:
        query = query.filter(Order.total_amount >= filters.min_amount)
    
    if filters.max_amount is not None:
        query = query.filter(Order.total_amount <= filters.max_amount)
    
    return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

def get_order_stats(db: Session, user_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
    """Obtener estadísticas de órdenes."""
    stats = {}
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Base de la consulta
    query = db.query(Order).filter(Order.created_at >= cutoff_date)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    # Total de órdenes
    stats["total_orders"] = query.count()
    
    # Total gastado
    total_amount = db.query(func.sum(Order.total_amount)).select_from(Order)
    total_amount = total_amount.filter(Order.created_at >= cutoff_date)
    if user_id:
        total_amount = total_amount.filter(Order.user_id == user_id)
    stats["total_amount"] = total_amount.scalar() or 0
    
    # Estadísticas por estado
    status_stats = db.query(
        Order.status, 
        func.count(Order.id).label("count"),
        func.sum(Order.total_amount).label("amount")
    ).filter(Order.created_at >= cutoff_date)
    
    if user_id:
        status_stats = status_stats.filter(Order.user_id == user_id)
    
    status_stats = status_stats.group_by(Order.status).all()
    
    stats["status"] = {
        status: {"count": count, "amount": amount or 0}
        for status, count, amount in status_stats
    }
    
    return stats 