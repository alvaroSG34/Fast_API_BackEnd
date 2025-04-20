-- Script para crear las tablas del carrito de compras

-- Crear tipo enumerado para estado del carrito
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'estado_carrito') THEN
        CREATE TYPE estado_carrito AS ENUM ('activo', 'guardado', 'procesado', 'abandonado');
    END IF;
END$$;

-- Tabla de Carrito de Compra
CREATE TABLE IF NOT EXISTS carritocompra (
    id_carrito SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES users(id) ON DELETE SET NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado estado_carrito DEFAULT 'activo',
    subtotal DECIMAL(10, 2) DEFAULT 0
);

-- Tabla de Detalle de Carrito
CREATE TABLE IF NOT EXISTS detallecarrito (
    id_detalle_carrito SERIAL PRIMARY KEY,
    id_carrito INTEGER REFERENCES carritocompra(id_carrito) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES products(id) ON DELETE RESTRICT,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    descuento DECIMAL(10, 2) DEFAULT 0,
    subtotal DECIMAL(10, 2) NOT NULL
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_carritocompra_usuario ON carritocompra(id_usuario);
CREATE INDEX IF NOT EXISTS idx_carritocompra_estado ON carritocompra(estado);
CREATE INDEX IF NOT EXISTS idx_detallecarrito_carrito ON detallecarrito(id_carrito);
CREATE INDEX IF NOT EXISTS idx_detallecarrito_producto ON detallecarrito(id_producto);

-- Datos de ejemplo para pruebas
INSERT INTO carritocompra (id_usuario, estado, subtotal)
SELECT id, 'activo', 0
FROM users
LIMIT 1
ON CONFLICT DO NOTHING;

-- Insertar algunos productos en el carrito del primer usuario
WITH first_cart AS (
    SELECT id_carrito FROM carritocompra ORDER BY id_carrito LIMIT 1
), 
random_products AS (
    SELECT id, precio_venta FROM products ORDER BY id LIMIT 3
)
INSERT INTO detallecarrito (id_carrito, id_producto, cantidad, precio_unitario, subtotal)
SELECT 
    (SELECT id_carrito FROM first_cart),
    id,
    1,
    precio_venta,
    precio_venta
FROM random_products
ON CONFLICT DO NOTHING;

-- Actualizar el subtotal del carrito
UPDATE carritocompra c
SET subtotal = (
    SELECT COALESCE(SUM(subtotal), 0)
    FROM detallecarrito
    WHERE id_carrito = c.id_carrito
)
WHERE EXISTS (
    SELECT 1
    FROM detallecarrito
    WHERE id_carrito = c.id_carrito
); 