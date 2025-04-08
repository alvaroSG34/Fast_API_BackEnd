from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user
from app.services import cart as cart_service
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, ApplyDiscount

router = APIRouter()

@router.get("/", response_model=CartResponse)
def get_active_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener el carrito activo del usuario autenticado."""
    cart = cart_service.get_active_cart(db, user_id=current_user.id)
    
    # Calcular el total
    total = cart_service.calculate_cart_total(db, cart_id=cart.id)
    
    # Crear respuesta con total calculado
    response = CartResponse.from_orm(cart)
    response.total = total
    
    return response

@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Añadir un producto al carrito."""
    try:
        cart_item = cart_service.add_item_to_cart(db, user_id=current_user.id, item=item)
        return {"detail": "Producto agregado al carrito", "item_id": cart_item.id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar producto: {str(e)}"
        )

@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar la cantidad de un producto en el carrito."""
    try:
        cart_item = cart_service.update_cart_item(
            db, user_id=current_user.id, item_id=item_id, item_update=item_update
        )
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item no encontrado en el carrito"
            )
        return {"detail": "Item actualizado correctamente"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar item: {str(e)}"
        )

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar un producto del carrito."""
    result = cart_service.remove_cart_item(db, user_id=current_user.id, item_id=item_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )
    return {"detail": "Item eliminado correctamente"}

@router.get("/total", response_model=Dict[str, float])
def get_cart_total(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calcular el total del carrito activo."""
    cart = cart_service.get_active_cart(db, user_id=current_user.id)
    total = cart_service.calculate_cart_total(db, cart_id=cart.id)
    return {"total": total}

@router.post("/apply-discount", response_model=Dict[str, Any])
def apply_discount_to_cart(
    discount_data: ApplyDiscount,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Aplicar un código de descuento al carrito."""
    try:
        # Verificar que el carrito pertenece al usuario
        cart = cart_service.get_cart(db, cart_id=discount_data.cart_id)
        if not cart or cart.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este carrito"
            )
        
        # Aplicar descuento
        new_total = cart_service.apply_discount(
            db, cart_id=discount_data.cart_id, discount_code=discount_data.discount_code
        )
        
        return {
            "detail": "Descuento aplicado correctamente",
            "discount_code": discount_data.discount_code,
            "new_total": new_total
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al aplicar descuento: {str(e)}"
        ) 