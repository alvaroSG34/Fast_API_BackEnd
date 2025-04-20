from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.services import recommendation_service

router = APIRouter()

@router.get("/product/{product_id}", response_model=List[Dict[str, Any]])
def get_recommendations_for_product(product_id: int, max_recommendations: int = 4, db: Session = Depends(get_db)):
    """
    Obtiene recomendaciones para un producto específico utilizando el algoritmo Apriori
    """
    try:
        return recommendation_service.get_recommendations_for_product(db, product_id, max_recommendations)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo recomendaciones: {str(e)}"
        )

@router.post("/cart", response_model=List[Dict[str, Any]])
def get_recommendations_for_cart(cart_items: List[int], max_recommendations: int = 4, db: Session = Depends(get_db)):
    """
    Obtiene recomendaciones basadas en los productos que ya están en el carrito
    """
    try:
        return recommendation_service.get_recommendations_for_cart(db, cart_items, max_recommendations)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo recomendaciones para el carrito: {str(e)}"
        ) 