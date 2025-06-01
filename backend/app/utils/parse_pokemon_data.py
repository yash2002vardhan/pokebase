from app.service.pokemon import get_pokemon_service


def assign_roles(stats, types):
    roles = []

    hp = stats.get("hp", 0)
    attack = stats.get("attack", 0)
    defense = stats.get("defense", 0)
    sp_atk = stats.get("special-attack", 0)
    sp_def = stats.get("special-defense", 0)
    speed = stats.get("speed", 0)

    total_stats = hp + attack + defense + sp_atk + sp_def + speed

    # Heuristic thresholds from percentiles
    is_fast = speed >= 92
    is_slow = speed <= 48
    is_physically_strong = attack >= 100
    is_special_strong = sp_atk >= 95
    is_physically_tanky = defense >= 95 or hp >= 85
    is_special_tanky = sp_def >= 90 or hp >= 85
    is_balanced = all([
        hp >= 70, attack >= 70, defense >= 70,
        sp_atk >= 65, sp_def >= 70, speed >= 70
    ])

    # Fast attacker
    if is_fast and (is_physically_strong or is_special_strong):
        roles.append("Sweeper")

    # Tank roles
    if is_physically_tanky or is_special_tanky:
        roles.append("Tank")

    # Glass cannon
    if (is_physically_strong or is_special_strong) and (defense <= 53 or sp_def <= 52):
        roles.append("Glass Cannon")

    # Support (based on type and low offensive power)
    support_types = {"fairy", "psychic", "grass"}
    if (speed <= 48 and attack <= 58 and sp_atk <= 50) or any(t in support_types for t in types):
        roles.append("Support")

    # Balanced
    if is_balanced:
        roles.append("Balanced")

    # If nothing fits, fallback role
    if not roles:
        roles.append("Generic")

    return list(set(roles))



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

    roles = assign_roles(pokemon_stats_dict, pokemon_types_list)

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
        "pokemon_height": height,
        "pokemon_id": pokemon_id,
        "pokemon_species": pokemon_species,
        "pokemon_weight": pokemon_weight,
        "role_type": roles,
    }

    return data
