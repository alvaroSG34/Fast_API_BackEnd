from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.inventory import Inventory
from sqlalchemy.orm import joinedload
from app.schemas.inventory import InventoryCreate, InventoryOut, InventoryUpdate

router = APIRouter()

@router.post("/", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
def create_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    if db.query(Inventory).filter(Inventory.id_producto == data.id_producto).first():
        raise HTTPException(status_code=400, detail="Este producto ya tiene inventario")
    inventario = Inventory(**data.dict())
    db.add(inventario)
    db.commit()
    db.refresh(inventario)
    return inventario

@router.get("/", response_model=list[InventoryOut])
def get_all_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).options(joinedload(Inventory.producto)).all()

@router.get("/{inventory_id}", response_model=InventoryOut)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inv = db.query(Inventory).get(inventory_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inv

@router.put("/{inventory_id}", response_model=InventoryOut)
def update_inventory(inventory_id: int, data: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(Inventory).get(inventory_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inv, key, value)

    db.commit()
    db.refresh(inv)
    return inv

