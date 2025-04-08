from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.services.product import get_product

def get_active_cart(db: Session, user_id: int) -> Cart:
    """Obtener el carrito activo del usuario o crear uno nuevo."""
    cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.is_active == 1).first()
    
    if not cart:
        # Crear un nuevo carrito si no existe uno activo
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart

def get_cart(db: Session, cart_id: int) -> Optional[Cart]:
    """Obtener un carrito por su ID."""
    return db.query(Cart).filter(Cart.id == cart_id).first()

def add_item_to_cart(db: Session, user_id: int, item: CartItemCreate) -> CartItem:
    """Añadir un producto al carrito."""
    # Obtener el carrito activo
    cart = get_active_cart(db, user_id)
    
    # Verificar si el producto existe y está activo
    product = get_product(db, item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado o no disponible"
        )
    
    # Verificar stock
    if product.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {product.stock}"
        )
    
    # Verificar si el producto ya está en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if cart_item:
        # Actualizar cantidad si ya existe
        cart_item.quantity += item.quantity
    else:
        # Crear nuevo item en el carrito
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item

def update_cart_item(db: Session, user_id: int, item_id: int, item_update: CartItemUpdate) -> Optional[CartItem]:
    """Actualizar la cantidad de un producto en el carrito."""
    # Obtener el carrito activo
    cart = get_active_cart(db, user_id)
    
    # Buscar el item en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        return None
    
    # Verificar stock
    product = get_product(db, cart_item.product_id)
    if not product or product.stock < item_update.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {product.stock if product else 0}"
        )
    
    # Actualizar cantidad
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def remove_cart_item(db: Session, user_id: int, item_id: int) -> bool:
    """Eliminar un producto del carrito."""
    # Obtener el carrito activo
    cart = get_active_cart(db, user_id)
    
    # Buscar el item en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        return False
    
    # Eliminar el item
    db.delete(cart_item)
    db.commit()
    return True

def calculate_cart_total(db: Session, cart_id: int) -> float:
    """Calcular el total del carrito."""
    cart = get_cart(db, cart_id)
    if not cart:
        return 0.0
    
    total = 0.0
    for item in cart.items:
        total += item.quantity * item.unit_price
    
    return total

def apply_discount(db: Session, cart_id: int, discount_code: str) -> float:
    """Aplicar un descuento al carrito y devolver el nuevo total."""
    # Esta es una función básica, se puede expandir para verificar códigos de descuento en la base de datos
    cart = get_cart(db, cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado"
        )
    
    # Ejemplo simple: código "DESCUENTO10" da 10% de descuento
    total = calculate_cart_total(db, cart_id)
    if discount_code == "DESCUENTO10":
        return total * 0.9  # 10% de descuento
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Código de descuento inválido"
    ) 