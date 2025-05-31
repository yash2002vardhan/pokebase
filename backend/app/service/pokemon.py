import aiohttp
from fastapi import Depends
from app.config.env import settings

class PokemonService:

    def __init__(self):
        self.base_url = settings.POKEMON_API_URL

    async def get_pokemon_data(self, pokemon_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/pokemon/{pokemon_name}") as response:
                if response.status == 404:
                    raise Exception(f"Pokemon {pokemon_name} not found")
                return await response.json()

    async def compare_pokemon(self, pokemon1: str, pokemon2: str):
        pokemon1_data = await self.get_pokemon_data(pokemon1)
        pokemon2_data = await self.get_pokemon_data(pokemon2)
        return pokemon1_data, pokemon2_data
    
    async def get_counter_strategy(self, pokemon1: str):
        pokemon1_data = await self.get_pokemon_data(pokemon1)
        return "This is the strategy"

    async def get_teamup_strategy(self, pokemon1: str):
        pokemon1_data = await self.get_pokemon_data(pokemon1)
        return "This is the strategy"
    
    async def create_team(self, user_query: str):
        pass

async def get_pokemon_service() -> PokemonService:
    return PokemonService()
