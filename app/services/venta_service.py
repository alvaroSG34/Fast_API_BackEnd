from sqlalchemy.orm import Session
from app.models.sale import Venta, DetalleVenta
from app.schemas.venta import VentaCreate

def crear_venta(db: Session, venta_data: VentaCreate):
    # Lógica de negocio aquí
    venta = Venta(
        numero_factura=venta_data.numero_factura,
        id_usuario=venta_data.id_usuario,
        fecha_venta=venta_data.fecha_venta,
        subtotal=venta_data.subtotal,
        descuento=venta_data.descuento,
        total=venta_data.total,
        metodo_pago=venta_data.metodo_pago,
        estado="completada",
    )
    db.add(venta)
    db.flush()

    for detalle in venta_data.detalles:
        db.add(DetalleVenta(
            id_venta=venta.id_venta,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            descuento=detalle.descuento,
            subtotal=detalle.subtotal,
        ))

    db.commit()
    db.refresh(venta)
    return venta
