from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.utils.parse_pokemon_data import parse_pokemon_data
from app.utils.prompts import strategy_prompt, team_creation_prompt
from app.config.llm import llm
from app.utils.generate_descriptions import generate_descriptions
import json
from fastapi import Body
# Create routers
pokemon_router = APIRouter()
health_router = APIRouter()


with open("all_pokemon_descriptions.json", "r") as f:
    pokemon_descriptions = json.load(f)

# Pokemon endpoints
@pokemon_router.get("/{pokemon_name}")
async def get_pokemon(
    pokemon_name: str
) -> str:
    try:
        pokemon_name = pokemon_name.lower()
        pokemon_data = await parse_pokemon_data(pokemon_name)
        pokemon_description = generate_descriptions(pokemon_data)
        return pokemon_description
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@pokemon_router.get("/compare/{pokemon1}/{pokemon2}")
async def compare_pokemon(
    pokemon1: str,
    pokemon2: str
) -> str:
    p1_data = await parse_pokemon_data(pokemon1)
    p2_data = await parse_pokemon_data(pokemon2)
    p1_description = generate_descriptions(p1_data)
    p2_description = generate_descriptions(p2_data)
    comparison_string = f"{p1_description}\n\n{p2_description}"  # Added extra newline
    return comparison_string

@pokemon_router.post("/strategy")
async def get_strategy(
    user_query: str = Body(...)
) ->  str | None:
    strategy_prompt_template = strategy_prompt.format(user_query=user_query, pokemon_description=pokemon_descriptions)
    return llm.generate_content(strategy_prompt_template)

@pokemon_router.post("/team-building")
async def get_team(
    user_query: str = Body(...)
) ->  str | None:
    team_creation_prompt_template = team_creation_prompt.format(user_query=user_query, pokemon_description=pokemon_descriptions)
    return llm.generate_content(team_creation_prompt_template)

# Health check endpoint
@health_router.get("")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
