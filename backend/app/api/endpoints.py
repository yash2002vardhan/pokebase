from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.utils.parse_pokemon_data import parse_pokemon_data
# Create routers
pokemon_router = APIRouter()
health_router = APIRouter()

# Pokemon endpoints
@pokemon_router.get("/{pokemon_name}")
async def get_pokemon(
    pokemon_name: str
) -> Dict[str, Any]:
    try:
        pokemon_name = pokemon_name.lower()
        return await parse_pokemon_data(pokemon_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@pokemon_router.get("/compare/{pokemon1}/{pokemon2}")
async def compare_pokemon(
    pokemon1: str,
    pokemon2: str
) -> Dict[str, Any]:
    return {
        "pokemon1": await parse_pokemon_data(pokemon1),
        "pokemon2": await parse_pokemon_data(pokemon2)
    }

# Health check endpoint
@health_router.get("")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
