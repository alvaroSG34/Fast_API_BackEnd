from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilter
from sqlalchemy import or_, and_

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Obtener un producto por su ID."""
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Obtener todos los productos activos."""
    return db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    """Crear un nuevo producto."""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    """Actualizar un producto existente."""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    """Eliminar un producto (desactivarlo)."""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db_product.is_active = False
    db.commit()
    return True

def filter_products(db: Session, filters: ProductFilter, skip: int = 0, limit: int = 100) -> List[Product]:
    """Filtrar productos según varios criterios."""
    query = db.query(Product).filter(Product.is_active == True)
    
    # Aplicar filtros si están presentes
    if filters.name:
        query = query.filter(Product.name.ilike(f"%{filters.name}%"))
    
    if filters.category:
        query = query.filter(Product.category == filters.category)
    
    if filters.min_price is not None:
        query = query.filter(Product.price >= filters.min_price)
    
    if filters.max_price is not None:
        query = query.filter(Product.price <= filters.max_price)
    
    if filters.in_stock is not None and filters.in_stock:
        query = query.filter(Product.stock > 0)
    
    return query.offset(skip).limit(limit).all()

def get_low_stock_products(db: Session, threshold: int = 5) -> List[Product]:
    """Obtener productos con bajo stock."""
    return db.query(Product).filter(
        Product.is_active == True,
        Product.stock <= threshold,
        Product.stock > 0
    ).all() 