import requests
from app.config.env import settings


class PokemonService:

    def __init__(self):
        self.base_url = settings.POKEMON_API_URL

    def get_pokemon_data(self, pokemon_name: str):
        response = requests.get(f"{self.base_url}/pokemon/{pokemon_name}")
        return response.json()

    def compare_pokemon(self, pokemon1: str, pokemon2: str):
        pokemon1_data = self.get_pokemon_data(pokemon1)
        pokemon2_data = self.get_pokemon_data(pokemon2)
        return pokemon1_data, pokemon2_data
    
    def get_counter_strategy(self, pokemon1: str):
        pokemon1_data = self.get_pokemon_data(pokemon1)
        return "This is the strategy"

    def get_teamup_strategy(self, pokemon1: str):
        pokemon1_data = self.get_pokemon_data(pokemon1)
        return "This is the strategy"
    
    def create_team(self, user_query: str):
        pass
