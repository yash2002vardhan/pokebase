from app.service.pokemon import get_pokemon_service


def get_roles(pokemon_stats_dict: dict) -> list:
    roles = []
    if pokemon_stats_dict["speed"] >= 90:
        roles.append("fast")
    if pokemon_stats_dict["attack"] >= 85:
        roles.append("physical-attacker")
    if pokemon_stats_dict["special-attack"] >= 90:
        roles.append("special-attacker")
    if pokemon_stats_dict["defense"] >= 90 or pokemon_stats_dict["special-defense"] >= 90:
        roles.append("tank")
    if pokemon_stats_dict["hp"] >= 80 and (pokemon_stats_dict["defense"] >= 80 or pokemon_stats_dict["special-defense"] >= 80):
        roles.append("defensive")
    return roles


async def parse_pokemon_data(pokemon_name: str) -> dict:
    service = await get_pokemon_service()
    pokemon_data = await service.get_pokemon_data(pokemon_name)

    abilities = pokemon_data.get("abilities", [])
    abilities_dict = {}
    for ability in abilities:
        ability_name = ability.get("ability", {}).get("name", "")
        hidden_status = ability.get("is_hidden", False)

        abilities_dict[ability_name] = hidden_status

    moves = pokemon_data.get("moves", [])
    moves_list = []
    for move in moves:
        move_name = move.get("move", {}).get("name", "")
        moves_list.append(move_name)

    pokemon_types = pokemon_data.get("types", [])
    pokemon_types_list = []
    for p_type in pokemon_types:
        type_name = p_type.get("type", {}).get("name", "")
        pokemon_types_list.append(type_name)

    pokemon_stats = pokemon_data.get("stats", [])
    pokemon_stats_dict = {}
    for stat in pokemon_stats:
        stat_name = stat.get("stat", {}).get("name", "")
        stat_value = stat.get("base_stat", None)
        pokemon_stats_dict[stat_name] = stat_value

    roles = get_roles(pokemon_stats_dict)

    base_experience = pokemon_data.get("base_experience", None)
    height = pokemon_data.get("height", None)

    pokemon_id = pokemon_data.get("id", None)
    pokemon_species = pokemon_data.get("species", {}).get("name", "")

    pokemon_weight = pokemon_data.get("weight", None)
    
    data = {
        "abilities": abilities_dict,
        "moves": moves_list,
        "types": pokemon_types_list,
        "stats": pokemon_stats_dict,
        "base_experience": base_experience,
        "height": height,
        "pokemon_id": pokemon_id,
        "pokemon_species": pokemon_species,
        "pokemon_weight": pokemon_weight,
        "role_type": roles,
    }

    return data
