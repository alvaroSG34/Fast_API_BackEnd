from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_active_user, get_current_user_with_permissions
from app.services import product as product_service
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, ProductFilter

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Crear un nuevo producto.
    Solo usuarios con permisos de administrador pueden crear productos.
    """
    return product_service.create_product(db=db, product=product)

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener lista de productos. Requiere autenticación."""
    products = product_service.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtener un producto específico. Requiere autenticación."""
    db_product = product_service.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Actualizar un producto existente.
    Solo usuarios con permisos de administrador pueden actualizar productos.
    """
    db_product = product_service.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin"]))
):
    """
    Eliminar (desactivar) un producto.
    Solo usuarios con permisos de administrador pueden eliminar productos.
    """
    result = product_service.delete_product(db, product_id=product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return {"detail": "Producto eliminado correctamente"}

@router.post("/filter", response_model=List[ProductResponse])
def filter_products(
    filters: ProductFilter,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Filtrar productos según varios criterios. Requiere autenticación."""
    products = product_service.filter_products(db, filters=filters, skip=skip, limit=limit)
    return products

@router.get("/inventory/low-stock", response_model=List[ProductResponse])
def get_low_stock(
    threshold: int = Query(5, description="Umbral de stock bajo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_permissions(["admin", "supervisor"]))
):
    """
    Obtener productos con stock bajo.
    Solo usuarios con permisos de administrador o supervisor pueden acceder.
    """
    products = product_service.get_low_stock_products(db, threshold=threshold)
    return products 