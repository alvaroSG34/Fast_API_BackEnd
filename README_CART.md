# Implementación del Carrito de Compras

Este documento describe la implementación del sistema de carrito de compras en el backend de la aplicación.

## Estructura de Archivos

Se han agregado los siguientes archivos:

1. **Modelos**:
   - `app/models/cart.py` - Modelo para la tabla `carritocompra`
   - `app/models/cart_item.py` - Modelo para la tabla `detallecarrito`

2. **Esquemas**:
   - `app/schemas/cart.py` - Esquemas Pydantic para el carrito
   - `app/schemas/cart_item.py` - Esquemas Pydantic para los items del carrito

3. **Servicios**:
   - `app/services/cart_service.py` - Funciones para manejar la lógica de negocio del carrito

4. **Rutas API**:
   - `app/api/v1/routes_cart.py` - Endpoints para el carrito

5. **Migración**:
   - `cart_migration.sql` - Script SQL para crear las tablas del carrito

## Endpoints Implementados

1. **Obtener carrito activo de un usuario**:
   ```
   GET /api/v1/carts/user/{user_id}/active
   ```
   - Devuelve el carrito activo del usuario o crea uno nuevo si no existe.

2. **Obtener items de un carrito**:
   ```
   GET /api/v1/carts/{cart_id}/items
   ```
   - Devuelve todos los items de un carrito específico con información detallada.

3. **Añadir item al carrito**:
   ```
   POST /api/v1/carts/items
   ```
   - Añade un producto al carrito. Si ya existe, incrementa la cantidad.

4. **Actualizar item del carrito**:
   ```
   PATCH /api/v1/carts/items/{item_id}
   ```
   - Actualiza la cantidad u otros atributos de un item.

5. **Eliminar item del carrito**:
   ```
   DELETE /api/v1/carts/items/{item_id}
   ```
   - Elimina un item del carrito.

6. **Procesar carrito (checkout)**:
   ```
   POST /api/v1/carts/{cart_id}/checkout
   ```
   - Procesa el carrito para convertirlo en una venta.

## Instrucciones de Instalación

1. **Actualizar la base de datos**:

   Ejecuta el script SQL para crear las tablas necesarias:
   ```bash
   psql -U tu_usuario -d tu_base_de_datos -f cart_migration.sql
   ```

2. **Reiniciar el servidor FastAPI**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Pruebas

Para probar los endpoints puedes usar:

1. La documentación de Swagger disponible en `/docs` cuando el servidor está en ejecución.
2. Herramientas como Postman o Thunder Client para realizar solicitudes HTTP directamente.

### Ejemplos de solicitudes:

1. **Obtener carrito activo**:
   ```
   GET http://localhost:8000/api/v1/carts/user/1/active
   ```

2. **Añadir producto al carrito**:
   ```
   POST http://localhost:8000/api/v1/carts/items
   
   {
     "id_carrito": 1,
     "id_producto": 1,
     "cantidad": 1,
     "precio_unitario": 29.99,
     "descuento": 0,
     "subtotal": 29.99
   }
   ```

3. **Actualizar cantidad**:
   ```
   PATCH http://localhost:8000/api/v1/carts/items/1
   
   {
     "cantidad": 2
   }
   ```

4. **Hacer checkout**:
   ```
   POST http://localhost:8000/api/v1/carts/1/checkout
   
   {
     "metodo_pago": "efectivo"
   }
   ```

## Notas Importantes

- El sistema actualiza automáticamente los subtotales cuando se modifican las cantidades.
- Se almacena el precio unitario en el momento de añadir al carrito para mantener un historial consistente.
- La lógica del checkout está simplificada, y se podría extender para crear una venta en el sistema. 