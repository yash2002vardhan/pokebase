from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.service.pokemon import get_pokemon_service, PokemonService

# Create routers
pokemon_router = APIRouter()
health_router = APIRouter()

# Pokemon endpoints
@pokemon_router.get("/{pokemon_name}")
async def get_pokemon(
    pokemon_name: str,
    pokemon_service: PokemonService = Depends(get_pokemon_service)
) -> Dict[str, Any]:
    try:
        pokemon_name = pokemon_name.lower()
        return await pokemon_service.get_pokemon_data(pokemon_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Health check endpoint
@health_router.get("")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
