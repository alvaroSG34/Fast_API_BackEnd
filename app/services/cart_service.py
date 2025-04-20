from sqlalchemy.orm import Session
from app.models.cart import CarritoCompra
from app.models.cart_item import DetalleCarrito
from app.models.product import Product
from app.schemas.cart import CartCreate
from app.schemas.cart_item import CartItemCreate, CartItemUpdate
from fastapi import HTTPException
import datetime
import traceback

def get_active_cart_for_user(db: Session, user_id: int):
    try:
        cart = db.query(CarritoCompra).filter(
            CarritoCompra.id_usuario == user_id,
            CarritoCompra.estado == "activo"
        ).first()
        
        if not cart:
            # Si no existe un carrito activo, lo creamos
            cart = CarritoCompra(
                id_usuario=user_id,
                estado="activo",
                subtotal=0.0,
                fecha_creacion=datetime.datetime.utcnow(),
                fecha_actualizacion=datetime.datetime.utcnow()
            )
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        return cart
    except Exception as e:
        print(f"Error en get_active_cart_for_user: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener el carrito: {str(e)}")

def get_cart_by_id(db: Session, cart_id: int):
    try:
        cart = db.query(CarritoCompra).filter(CarritoCompra.id_carrito == cart_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Carrito no encontrado")
        return cart
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_cart_by_id: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener el carrito: {str(e)}")

def get_cart_items(db: Session, cart_id: int):
    try:
        # Asegurar que el carrito existe
        cart = get_cart_by_id(db, cart_id)
        
        # Consulta que incluye nombre e imagen del producto
        items = db.query(
            DetalleCarrito,
            Product.nombre.label("nombre_producto"),
            Product.imagen.label("imagen_producto")
        ).join(
            Product, DetalleCarrito.id_producto == Product.id
        ).filter(
            DetalleCarrito.id_carrito == cart_id
        ).all()
        
        # Transformar resultados a un formato adecuado
        result = []
        for item, nombre_producto, imagen_producto in items:
            item_dict = {
                "id": item.id_detalle_carrito,
                "id_carrito": item.id_carrito,
                "id_producto": item.id_producto,
                "cantidad": item.cantidad,
                "precio_unitario": item.precio_unitario,
                "descuento": item.descuento,
                "subtotal": item.subtotal,
                "nombre_producto": nombre_producto,
                "imagen_producto": imagen_producto
            }
            result.append(item_dict)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_cart_items: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al obtener los items del carrito: {str(e)}")

def add_item_to_cart(db: Session, item_data: CartItemCreate):
    try:
        # Verificar si el producto existe
        product = db.query(Product).filter(Product.id == item_data.id_producto).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Verificar si el carrito existe
        cart = get_cart_by_id(db, item_data.id_carrito)
        
        # Verificar si el item ya existe en el carrito
        existing_item = db.query(DetalleCarrito).filter(
            DetalleCarrito.id_carrito == item_data.id_carrito,
            DetalleCarrito.id_producto == item_data.id_producto
        ).first()
        
        if existing_item:
            # Actualizar cantidad y subtotal si ya existe
            existing_item.cantidad += item_data.cantidad
            existing_item.subtotal = (existing_item.precio_unitario * existing_item.cantidad) - existing_item.descuento
            db.commit()
            db.refresh(existing_item)
            item = existing_item
        else:
            # Crear nuevo item con el precio actual del producto
            precio = product.precio_venta
            subtotal = (precio * item_data.cantidad) - item_data.descuento
            
            item = DetalleCarrito(
                id_carrito=item_data.id_carrito,
                id_producto=item_data.id_producto,
                cantidad=item_data.cantidad,
                precio_unitario=precio,
                descuento=item_data.descuento,
                subtotal=subtotal
            )
            db.add(item)
            db.commit()
            db.refresh(item)
        
        # Actualizar el subtotal del carrito
        cart = update_cart_subtotal(db, cart.id_carrito)
        
        # Obtener datos adicionales del producto para la respuesta
        return {
            "id": item.id_detalle_carrito,
            "id_carrito": item.id_carrito,
            "id_producto": item.id_producto,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "descuento": item.descuento,
            "subtotal": item.subtotal,
            "nombre_producto": product.nombre,
            "imagen_producto": product.imagen
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en add_item_to_cart: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al agregar item al carrito: {str(e)}")

def update_cart_item(db: Session, item_id: int, item_data: CartItemUpdate):
    try:
        item = db.query(DetalleCarrito).filter(DetalleCarrito.id_detalle_carrito == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        
        # Actualizar campos si se proporcionan
        if item_data.cantidad is not None:
            item.cantidad = item_data.cantidad
        
        if item_data.descuento is not None:
            item.descuento = item_data.descuento
        
        # Calcular subtotal
        item.subtotal = (item.precio_unitario * item.cantidad) - item.descuento
        
        db.commit()
        db.refresh(item)
        
        # Actualizar el subtotal del carrito
        update_cart_subtotal(db, item.id_carrito)
        
        # Obtener datos adicionales del producto
        product = db.query(Product).filter(Product.id == item.id_producto).first()
        
        result = {
            "id": item.id_detalle_carrito,
            "id_carrito": item.id_carrito,
            "id_producto": item.id_producto,
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "descuento": item.descuento,
            "subtotal": item.subtotal,
            "nombre_producto": product.nombre if product else None,
            "imagen_producto": product.imagen if product else None
        }
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en update_cart_item: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el item: {str(e)}")

def remove_cart_item(db: Session, item_id: int):
    try:
        item = db.query(DetalleCarrito).filter(DetalleCarrito.id_detalle_carrito == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        
        cart_id = item.id_carrito
        
        db.delete(item)
        db.commit()
        
        # Actualizar el subtotal del carrito
        update_cart_subtotal(db, cart_id)
        
        return {"message": "Item eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en remove_cart_item: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el item: {str(e)}")

def update_cart_subtotal(db: Session, cart_id: int):
    try:
        cart = get_cart_by_id(db, cart_id)
        
        # Calcular subtotal sumando todos los items
        # 1. Primero intentar con SQL directo para evitar errores con db.func
        try:
            result = db.execute(
                "SELECT COALESCE(SUM(subtotal), 0) as total FROM detalle_carrito WHERE id_carrito = :cart_id",
                {"cart_id": cart_id}
            ).fetchone()
            
            if result and hasattr(result, 'total'):
                subtotal = float(result.total)
            else:
                # 2. Alternativa: usar una suma manual en Python
                items = db.query(DetalleCarrito).filter(DetalleCarrito.id_carrito == cart_id).all()
                subtotal = sum(item.subtotal for item in items) if items else 0.0
        except Exception as sql_error:
            print(f"Error en SQL de subtotal, usando alternativa: {str(sql_error)}")
            # 3. Alternativa en caso de error: usar una suma manual
            items = db.query(DetalleCarrito).filter(DetalleCarrito.id_carrito == cart_id).all()
            subtotal = sum(item.subtotal for item in items) if items else 0.0
        
        cart.subtotal = subtotal
        cart.fecha_actualizacion = datetime.datetime.utcnow()
        
        db.commit()
        db.refresh(cart)
        
        return cart
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en update_cart_subtotal: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        
        # En caso de error, intentar manejar silenciosamente para que la UI no se bloquee
        try:
            # Recuperar el carrito sin actualizar el subtotal
            cart = db.query(CarritoCompra).filter(CarritoCompra.id_carrito == cart_id).first()
            if cart:
                return cart
        except:
            pass
            
        # Si todo falla, propagar el error
        raise HTTPException(status_code=500, detail=f"Error al actualizar el subtotal: {str(e)}")

def process_cart_checkout(db: Session, cart_id: int, metodo_pago: str):
    try:
        cart = get_cart_by_id(db, cart_id)
        
        if cart.estado != "activo":
            raise HTTPException(status_code=400, detail="El carrito no está en estado activo para procesar")
        
        # Verificar si el carrito tiene items
        if cart.subtotal <= 0:
            raise HTTPException(status_code=400, detail="El carrito está vacío")
        
        # Aquí iría la lógica para crear una venta en base al carrito
        # Por ahora, solo marcamos el carrito como procesado
        
        cart.estado = "procesado"
        cart.fecha_actualizacion = datetime.datetime.utcnow()
        
        db.commit()
        db.refresh(cart)
        
        return {"message": "Carrito procesado correctamente", "cart_id": cart.id_carrito}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en process_cart_checkout: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el carrito: {str(e)}") 