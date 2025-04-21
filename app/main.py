from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1 import routes_user, routes_auth
from app.api.v1.routes_role import router as role_router
from app.core.config import settings
from app.api.v1.routes_category import router as category_router
from app.api.v1.routes_product import router as product_router
from app.api.v1.routes_inventory import router as inventory_router
from app.api.v1.routes_proveedor import router as proveedor_router
from app.api.v1.routes_producto_proveedor import router as producto_proveedor_router
from app.api.v1.routes_cart import router as cart_router
from app.api.v1.routes_recommendations import router as recommendations_router
from app.api.v1.routes_stripe import router as stripe_router
from app.api.v1.routes_sale import router as sale_router
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://frontend-pos-production.up.railway.app/",
    "http://localhost:5173",  # mantenerlo para pruebas locales si quieres
],  # 👈 Permitir cualquier origen para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(routes_user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(role_router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(category_router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(product_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(inventory_router, prefix="/api/v1/inventario", tags=["Inventario"])
app.include_router(proveedor_router, prefix="/api/v1/proveedores", tags=["Proveedores"])
app.include_router(producto_proveedor_router, prefix="/api/v1/producto-proveedor", tags=["ProductoProveedor"])
app.include_router(cart_router, prefix="/api/v1/carts", tags=["Carritos"])
app.include_router(recommendations_router, prefix="/api/v1/recommendations", tags=["Recomendaciones"])
app.include_router(stripe_router, prefix="/api/v1/stripe", tags=["Stripe"])
app.include_router(sale_router, prefix="/api/v1/sales", tags=["Ventas"])

# 👉 Custom OpenAPI para habilitar el botón Authorize con JWT Bearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sistema POS Inteligente",
        version="1.0.0",
        description="API para gestión de usuarios, roles y ventas",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Aplica el esquema de seguridad a todas las rutas
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
