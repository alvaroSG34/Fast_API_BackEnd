from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.producto_proveedor import ProductoProveedor
from app.models.proveedor import Proveedor
from sqlalchemy.orm import Session, joinedload
from app.schemas.producto_proveedor import ProductoProveedorOut
from app.schemas.proveedor import ProveedorCreate, ProveedorOut

router = APIRouter()

@router.post("/", response_model=ProveedorOut, status_code=status.HTTP_201_CREATED)
def create_proveedor(data: ProveedorCreate, db: Session = Depends(get_db)):
    proveedor = Proveedor(**data.dict())
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

@router.get("/", response_model=list[ProveedorOut])
def get_proveedores(db: Session = Depends(get_db)):
    return db.query(Proveedor).all()

@router.get("/", response_model=List[ProductoProveedorOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(ProductoProveedor)\
             .options(joinedload(ProductoProveedor.producto), joinedload(ProductoProveedor.proveedor))\
             .all()

@router.delete("/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedor).get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()

from app.schemas.proveedor import ProveedorUpdate

@router.put("/{proveedor_id}", response_model=ProveedorOut)
def update_proveedor(proveedor_id: int, data: ProveedorUpdate, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedor).get(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(proveedor, key, value)

    db.commit()
    db.refresh(proveedor)
    return proveedor
