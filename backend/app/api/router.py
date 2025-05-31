from fastapi import APIRouter

router = APIRouter()

router.get("/pokemon/{pokemon_name}")(PokemonService.get_pokemon)
