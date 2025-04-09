from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import (
    routes_user, 
    routes_auth, 
    routes_product, 
    routes_cart,
    routes_order,
    routes_report,
    routes_recommendation
)
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIs Iteración 1 - Autenticación y usuarios
app.include_router(routes_user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])

# APIs Iteración 2 - Administración e inventario
app.include_router(routes_product.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(routes_cart.router, prefix="/api/v1/cart", tags=["Cart"])

# APIs Iteración 3 - Reportes y recomendaciones
app.include_router(routes_order.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(routes_report.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(routes_recommendation.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
