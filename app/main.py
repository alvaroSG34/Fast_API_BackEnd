from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import routes_user, routes_auth, routes_product, routes_cart
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes_product.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(routes_cart.router, prefix="/api/v1/cart", tags=["Cart"])
