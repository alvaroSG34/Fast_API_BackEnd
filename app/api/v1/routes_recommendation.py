from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.models.user import User
from app.models.recommendation import ProductRecommendation, ProductAssociation
from app.core.security import get_current_active_user, get_current_user_with_permissions
from app.services import recommendation as recommendation_service
from app.schemas.recommendation import ProductRecommendationResponse, ProductAssociationCreate, ProductAssociationResponse, RecommendationParams
from app.schemas.product import ProductResponse

router = APIRouter()

@router.get("/products/for-user", response_model=List[ProductRecommendationResponse])
def get_recommendations_for_current_user(
    params: RecommendationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener recomendaciones de productos para el usuario autenticado."""
    recommendations = recommendation_service.get_product_recommendations(
        db, 
        user_id=current_user.id,
        limit=params.limit,
        min_score=params.min_score,
        include_viewed=params.include_viewed
    )
    return recommendations

@router.get("/products/with-product/{product_id}", response_model=List[ProductAssociationResponse])
def get_product_associations(
    product_id: int,
    limit: int = 5,
    min_strength: float = 0.1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener productos asociados a un producto específico."""
    associations = recommendation_service.get_product_associations(
        db, 
        product_id=product_id,
        limit=limit,
        min_strength=min_strength
    )
    return associations

@router.post("/products/associations", response_model=ProductAssociationResponse, status_code=status.HTTP_201_CREATED)
def create_product_association(
    association: ProductAssociationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Crear manualmente una asociación entre productos.
    Solo administradores pueden crear asociaciones.
    """
    return recommendation_service.create_product_association(db, association=association)

@router.post("/products/mark-viewed/{recommendation_id}")
def mark_recommendation_as_viewed(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marcar una recomendación como vista."""
    # Primero verificar que la recomendación pertenece al usuario
    recommendation = db.query(ProductRecommendation).filter(
        ProductRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recomendación no encontrada"
        )
    
    if recommendation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta recomendación"
        )
    
    success = recommendation_service.mark_recommendation_as_viewed(db, recommendation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al marcar la recomendación como vista"
        )
    
    return {"detail": "Recomendación marcada como vista correctamente"}

@router.post("/generate-recommendations", status_code=status.HTTP_202_ACCEPTED)
def generate_recommendations(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Generar recomendaciones para un usuario basado en su historial de compras.
    Solo administradores pueden ejecutar este proceso.
    """
    # Este proceso puede ser costoso, por lo que lo ejecutamos en segundo plano
    background_tasks.add_task(recommendation_service.update_product_associations_from_orders, db)
    
    return {"detail": "Proceso de generación de recomendaciones iniciado en segundo plano"}

@router.post("/generate-for-user/{user_id}", response_model=List[ProductRecommendationResponse])
def generate_recommendations_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Generar recomendaciones para un usuario específico.
    Solo administradores pueden ejecutar este proceso.
    """
    recommendations = recommendation_service.generate_recommendations(db, user_id=user_id)
    return recommendations 