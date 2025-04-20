from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 👇 Importa todos los modelos aquí para que Alembic los vea
from app.models.user import User
from app.models.role import Role
from app.models.category import Category
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.proveedor import Proveedor
from app.models.producto_proveedor import ProductoProveedor
from app.models.sale import Venta
from app.models.sale_detail import DetalleVenta



# Importá otros modelos si los tenés (ej: Product, Permission, etc.)
