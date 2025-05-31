from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.utils.parse_pokemon_data import parse_pokemon_data
from app.utils.prompts import strategy_prompt
from app.config.llm import llm
import json
# Create routers
pokemon_router = APIRouter()
health_router = APIRouter()


with open("all_pokemon_descriptions.json", "r") as f:
    pokemon_descriptions = json.load(f)

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

@pokemon_router.post("/strategy")
async def get_strategy(
    user_query: str
) ->  str | None:
    strategy_prompt_template = strategy_prompt.format(user_query=user_query, pokemon_description=pokemon_descriptions)
    return llm.generate_content(strategy_prompt_template)
    
# Health check endpoint
@health_router.get("")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
