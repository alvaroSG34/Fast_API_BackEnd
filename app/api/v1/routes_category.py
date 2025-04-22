from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.schemas.category import CategoryUpdate
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter()

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    category = Category(**data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(category)
    db.commit()

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    category.name = data.name
    category.description = data.description
    db.commit()
    db.refresh(category)
    return category    

@router.get("/{category_id}/products", response_model=list[ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    products = db.query(Product).filter(Product.id_categoria == category_id).all()
    return products    
