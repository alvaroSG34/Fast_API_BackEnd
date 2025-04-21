from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.schemas.sale import VentaCreate
from app.services import sale_service
from app.services.sale_service import crear_venta, get_sales_report
from app.schemas.sale import FacturaVenta
from app.schemas.sale import VentaResumen
from app.db.session import get_db
from app.schemas.sale import DetalleVentaOut

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    try:
        return crear_venta(db, venta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", response_model=List[VentaResumen])
def obtener_ventas(db: Session = Depends(get_db)):
    return sale_service.listar_ventas(db)    

@router.get("/{id_venta}/detalle", response_model=List[DetalleVentaOut])
def obtener_detalle(id_venta: int, db: Session = Depends(get_db)):
    return sale_service.obtener_detalle_por_venta(db, id_venta)

@router.get("/{id_venta}/detalle", response_model=FacturaVenta)
def obtener_detalle(id_venta: int, db: Session = Depends(get_db)):
    return sale_service.obtener_factura_completa(db, id_venta)

@router.get("/reportes", response_model=List[dict])
def reportes_ventas(
    cliente: Optional[str] = Query(None),
    fecha_inicio: Optional[date] = Query(None),
    fecha_fin: Optional[date] = Query(None),
    categoria: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return get_sales_report(db, cliente, fecha_inicio, fecha_fin, categoria)
