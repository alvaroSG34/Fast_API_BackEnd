from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.recommendation import ProductRecommendation, ProductAssociation
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.recommendation import ProductAssociationCreate
from sqlalchemy import and_, or_, func, desc

def get_product_recommendations(db: Session, user_id: int, limit: int = 5, min_score: float = 0.0, include_viewed: bool = False) -> List[ProductRecommendation]:
    """Obtener recomendaciones de productos para un usuario."""
    query = db.query(ProductRecommendation).filter(
        ProductRecommendation.user_id == user_id,
        ProductRecommendation.score >= min_score
    )
    
    if not include_viewed:
        query = query.filter(ProductRecommendation.is_viewed == False)
    
    return query.order_by(ProductRecommendation.score.desc()).limit(limit).all()

def mark_recommendation_as_viewed(db: Session, recommendation_id: int) -> bool:
    """Marcar una recomendación como vista."""
    recommendation = db.query(ProductRecommendation).filter(
        ProductRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        return False
    
    recommendation.is_viewed = True
    db.commit()
    return True

def get_product_associations(db: Session, product_id: int, limit: int = 5, min_strength: float = 0.0) -> List[ProductAssociation]:
    """Obtener productos asociados a un producto."""
    return db.query(ProductAssociation).filter(
        ProductAssociation.product_id == product_id,
        ProductAssociation.strength >= min_strength
    ).order_by(ProductAssociation.strength.desc()).limit(limit).all()

def create_product_association(db: Session, association: ProductAssociationCreate) -> ProductAssociation:
    """Crear una asociación entre productos."""
    # Verificar que los productos existen
    product = db.query(Product).filter(Product.id == association.product_id).first()
    associated_product = db.query(Product).filter(Product.id == association.associated_product_id).first()
    
    if not product or not associated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uno o ambos productos no existen"
        )
    
    # Verificar que no sea el mismo producto
    if association.product_id == association.associated_product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede asociar un producto consigo mismo"
        )
    
    # Verificar si ya existe una asociación
    existing = db.query(ProductAssociation).filter(
        ProductAssociation.product_id == association.product_id,
        ProductAssociation.associated_product_id == association.associated_product_id
    ).first()
    
    if existing:
        # Actualizar fuerza de asociación existente
        existing.strength = association.strength
        db.commit()
        db.refresh(existing)
        return existing
    
    # Crear nueva asociación
    db_association = ProductAssociation(**association.dict())
    db.add(db_association)
    db.commit()
    db.refresh(db_association)
    return db_association

def generate_recommendations(db: Session, user_id: int) -> List[ProductRecommendation]:
    """Generar recomendaciones para un usuario basado en su historial de compras."""
    # 1. Obtener productos que el usuario ha comprado
    user_products = db.query(OrderItem.product_id, func.sum(OrderItem.quantity).label("quantity"))\
        .join(Order, Order.id == OrderItem.order_id)\
        .filter(Order.user_id == user_id)\
        .group_by(OrderItem.product_id)\
        .all()
    
    user_product_ids = [p.product_id for p in user_products]
    
    # No hay suficientes datos para generar recomendaciones
    if not user_product_ids:
        return []
    
    # 2. Encontrar productos asociados a los que el usuario ha comprado
    associated_products = db.query(
        ProductAssociation.associated_product_id,
        func.max(ProductAssociation.strength).label("max_strength")
    ).filter(
        ProductAssociation.product_id.in_(user_product_ids),
        ~ProductAssociation.associated_product_id.in_(user_product_ids)  # Excluir productos ya comprados
    ).group_by(ProductAssociation.associated_product_id)\
    .order_by(func.max(ProductAssociation.strength).desc())\
    .limit(10)\
    .all()
    
    # 3. Crear o actualizar recomendaciones para el usuario
    recommendations = []
    for prod in associated_products:
        # Verificar si ya existe una recomendación
        existing = db.query(ProductRecommendation).filter(
            ProductRecommendation.user_id == user_id,
            ProductRecommendation.product_id == prod.associated_product_id
        ).first()
        
        if existing:
            # Actualizar score
            existing.score = prod.max_strength
            existing.is_viewed = False  # Resetear vista ya que hay un nuevo score
            existing.updated_at = func.now()
            db.commit()
            db.refresh(existing)
            recommendations.append(existing)
        else:
            # Crear nueva recomendación
            new_rec = ProductRecommendation(
                user_id=user_id,
                product_id=prod.associated_product_id,
                score=prod.max_strength
            )
            db.add(new_rec)
            db.commit()
            db.refresh(new_rec)
            recommendations.append(new_rec)
    
    return recommendations

def update_product_associations_from_orders(db: Session) -> int:
    """Actualizar asociaciones de productos basado en órdenes existentes.
    Retorna el número de asociaciones creadas o actualizadas."""
    
    # Encontrar productos que se compran juntos
    paired_products = db.query(
        oi1.product_id.label("product_id"),
        oi2.product_id.label("associated_product_id"),
        func.count(oi1.order_id).label("frequency")
    ).select_from(OrderItem.alias("oi1"), OrderItem.alias("oi2"))\
    .filter(
        oi1.order_id == oi2.order_id,
        oi1.product_id < oi2.product_id  # Evitar duplicados (A,B) y (B,A)
    ).group_by(oi1.product_id, oi2.product_id)\
    .having(func.count(oi1.order_id) > 1)  # Al menos aparecen juntos más de una vez
    
    # Calcular el máximo para normalizar
    max_frequency = db.query(func.max(paired_products.c.frequency)).scalar() or 1
    
    # Crear/actualizar asociaciones
    count = 0
    for p in paired_products:
        strength = p.frequency / max_frequency
        
        # Crear asociación en ambas direcciones
        for product_id, associated_id in [(p.product_id, p.associated_product_id), 
                                         (p.associated_product_id, p.product_id)]:
            existing = db.query(ProductAssociation).filter(
                ProductAssociation.product_id == product_id,
                ProductAssociation.associated_product_id == associated_id
            ).first()
            
            if existing:
                existing.strength = strength
            else:
                db.add(ProductAssociation(
                    product_id=product_id,
                    associated_product_id=associated_id,
                    strength=strength
                ))
                count += 1
    
    db.commit()
    return count 