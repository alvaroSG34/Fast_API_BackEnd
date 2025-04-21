from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime

from app.models.product import Product
from app.models.sale import Venta
from app.models.sale_detail import DetalleVenta  # ← import correcto
from app.models.user import User
from app.schemas.sale import VentaCreate

def generar_numero_factura(db: Session) -> str:
    """
    Genera un número de factura en formato FACT-000001.
    """
    ultimo_id = db.query(func.max(Venta.id_venta)).scalar() or 0
    nuevo_numero = ultimo_id + 1
    return f"FACT-{nuevo_numero:06d}"

def crear_venta(db: Session, venta_data: VentaCreate):
    """
    Registra una venta y sus detalles en la base de datos.
    """
    numero_factura = generar_numero_factura(db)

    venta = Venta(
        numero_factura=numero_factura,
        id_usuario=venta_data.id_usuario,
        fecha_venta=venta_data.fecha_venta,
        subtotal=venta_data.subtotal,
        descuento=venta_data.descuento,
        total=venta_data.total,
        metodo_pago=venta_data.metodo_pago,
        estado="completada",
    )
    db.add(venta)
    db.flush()  # Obtener el id_venta generado

    for detalle in venta_data.detalles:
        detalle_model = DetalleVenta(
            id_venta=venta.id_venta,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            descuento=detalle.descuento,
            subtotal=detalle.subtotal
        )
        db.add(detalle_model)

    db.commit()
    db.refresh(venta)
    return venta


def listar_ventas(db: Session):
    from app.models.sale import Venta
    from app.models.user import User

    ventas = (
        db.query(Venta, User)
        .join(User, Venta.id_usuario == User.id)
        .order_by(Venta.fecha_venta.desc())
        .all()
    )

    result = []
    for venta, usuario in ventas:
        result.append({
            "id_venta": venta.id_venta,
            "numero_factura": venta.numero_factura,
            "fecha_venta": venta.fecha_venta,
            "total": float(venta.total),
            "metodo_pago": venta.metodo_pago,
            "estado": venta.estado,
            "cliente": f"{usuario.nombre} {usuario.apellido}",
        })
    return result

def obtener_detalle_por_venta(db: Session, id_venta: int):
    from app.models.sale_detail import DetalleVenta
    from app.models.product import Product

    detalles = (
        db.query(DetalleVenta, Product)
        .join(Product, DetalleVenta.id_producto == Product.id)
        .filter(DetalleVenta.id_venta == id_venta)
        .all()
    )

    return [
        {
            "id_producto": p.id,
            "nombre": p.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": float(d.precio_unitario),
            "subtotal": float(d.subtotal),
        }
        for d, p in detalles
    ]

def obtener_factura_completa(db: Session, id_venta: int):
    from app.models.sale import Venta
    from app.models.sale_detail import DetalleVenta
    from app.models.product import Product
    from app.models.user import User

    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    usuario = db.query(User).filter(User.id == venta.id_usuario).first()

    detalles = (
        db.query(DetalleVenta, Product)
        .join(Product, DetalleVenta.id_producto == Product.id)
        .filter(DetalleVenta.id_venta == id_venta)
        .all()
    )

    items = [
        {
            "id_producto": p.id,
            "nombre": p.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": float(d.precio_unitario),
            "subtotal": float(d.subtotal),
        }
        for d, p in detalles
    ]

    return {
        "numero_factura": venta.numero_factura,
        "cliente": f"{usuario.nombre} {usuario.apellido}" if usuario else "Cliente",
        "fecha_venta": venta.fecha_venta,
        "metodo_pago": venta.metodo_pago,
        "estado": venta.estado,
        "subtotal": float(venta.subtotal),
        "descuento": float(venta.descuento),
        "total": float(venta.total),
        "items": items,
    }


def get_sales_report(
    db: Session,
    cliente: Optional[str],
    fecha_inicio: Optional[date],
    fecha_fin: Optional[date],
    categoria_id: Optional[int],
) -> List[dict]:
    query = db.query(Venta).join(User).filter(Venta.estado == "completada")

    if cliente:
        query = query.filter(User.nombre.ilike(f"%{cliente}%"))

    if fecha_inicio:
        query = query.filter(Venta.fecha_venta >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Venta.fecha_venta <= fecha_fin)

    ventas = query.all()

    resultado = []

    for venta in ventas:
        if categoria_id:
            tiene_categoria = db.query(DetalleVenta).join(Product).filter(
                DetalleVenta.id_venta == venta.id_venta,
                DetalleVenta.id_producto == Product.id,
                Product.id_categoria == categoria_id
            ).first()
            if not tiene_categoria:
                continue  # omitir esta venta

        resultado.append({
            "id_venta": venta.id_venta,
            "numero_factura": venta.numero_factura,
            "fecha_venta": venta.fecha_venta,
            "total": float(venta.total),
            "metodo_pago": venta.metodo_pago,
            "estado": venta.estado,
            "cliente": f"{venta.usuario.nombre} {venta.usuario.apellido}"
        })

    return resultado



