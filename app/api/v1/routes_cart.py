from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import cart_service
from app.schemas.cart import CartOut, CartCreate, CartUpdate
from app.schemas.cart_item import CartItemCreate, CartItemOut, CartItemUpdate
from typing import List

router = APIRouter()

# 1. Obtener el carrito activo de un usuario
@router.get("/user/{user_id}/active", response_model=CartOut)
def get_active_cart(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el carrito activo del usuario o crea uno nuevo si no existe.
    """
    return cart_service.get_active_cart_for_user(db, user_id)

# 2. Obtener los items de un carrito
@router.get("/{cart_id}/items", response_model=List[dict])
def get_cart_items(cart_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los items de un carrito específico.
    """
    return cart_service.get_cart_items(db, cart_id)

# 3. Añadir un item al carrito
@router.post("/items", response_model=dict)
def add_cart_item(item: CartItemCreate, db: Session = Depends(get_db)):
    """
    Añade un producto al carrito. Si ya existe, incrementa la cantidad.
    """
    return cart_service.add_item_to_cart(db, item)

# 4. Actualizar un item del carrito
@router.patch("/cart-items/{item_id}", response_model=dict)
def update_cart_item(item_id: int, item_data: CartItemUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la cantidad u otros atributos de un item del carrito.
    """
    return cart_service.update_cart_item(db, item_id, item_data)

# 5. Eliminar un item del carrito
@router.delete("/cart-items/{item_id}", response_model=dict)
def remove_cart_item(item_id: int, db: Session = Depends(get_db)):
    """
    Elimina un item del carrito.
    """
    return cart_service.remove_cart_item(db, item_id)

# 6. Procesar el carrito (checkout)
@router.post("/{cart_id}/checkout", response_model=dict)
def checkout_cart(cart_id: int, data: dict, db: Session = Depends(get_db)):
    """
    Procesa el carrito para convertirlo en una venta.
    """
    if "metodo_pago" not in data:
        raise HTTPException(status_code=400, detail="Método de pago es requerido")
    
    return cart_service.process_cart_checkout(db, cart_id, data["metodo_pago"]) 