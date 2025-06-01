import aiohttp
from fastapi import Depends
from app.config.env import settings
from app.config.logging import setup_logger

logger = setup_logger("pokemon_service")

class PokemonService:

    def __init__(self):
        self.base_url = settings.POKEMON_API_URL

    async def get_pokemon_data(self, pokemon_name: str):
        logger.info(f"Fetching Pokemon data for: {pokemon_name}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/pokemon/{pokemon_name}") as response:
                    if response.status == 404:
                        logger.error(f"Pokemon not found: {pokemon_name}")
                        raise Exception(f"Pokemon {pokemon_name} not found")
                    data = await response.json()
                    logger.info(f"Successfully fetched data for Pokemon: {pokemon_name}")
                    return data
        except Exception as e:
            logger.error(f"Error fetching Pokemon data: {str(e)}", exc_info=True)
            raise

async def get_pokemon_service() -> PokemonService:
    return PokemonService()
