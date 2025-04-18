from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.producto_proveedor import ProductoProveedor
from app.schemas.producto_proveedor import ProductoProveedorCreate, ProductoProveedorOut

router = APIRouter()

@router.post("/", response_model=ProductoProveedorOut, status_code=status.HTTP_201_CREATED)
def create_pp(data: ProductoProveedorCreate, db: Session = Depends(get_db)):
    pp = ProductoProveedor(**data.dict())
    db.add(pp)
    db.commit()
    db.refresh(pp)
    return pp

@router.get("/", response_model=list[ProductoProveedorOut])
def get_all_pp(db: Session = Depends(get_db)):
    return db.query(ProductoProveedor).all()

@router.get("/{pp_id}", response_model=ProductoProveedorOut)
def get_pp(pp_id: int, db: Session = Depends(get_db)):
    pp = db.query(ProductoProveedor).get(pp_id)
    if not pp:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return pp

@router.delete("/{pp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pp(pp_id: int, db: Session = Depends(get_db)):
    pp = db.query(ProductoProveedor).get(pp_id)
    if not pp:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(pp)
    db.commit()
