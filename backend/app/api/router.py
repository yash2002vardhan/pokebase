from fastapi import APIRouter
from .endpoints import pokemon_router, health_router

api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(pokemon_router, prefix="/pokemon", tags=["pokemon"])
api_router.include_router(health_router, prefix="/health", tags=["health"])
