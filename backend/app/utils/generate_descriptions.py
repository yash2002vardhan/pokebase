import json

def format_list(items):
    """Formats a list as a comma-separated string with proper grammar."""
    return ', '.join(items)

def capitalize_list(items):
    """Capitalizes the first letter of each item in a list."""
    return [item.capitalize() for item in items]

with open("all_parsed_data.json", "r") as f:
    data = json.load(f)

description_template = (
    "{name} is a {pokemon_type} type Pokémon with the standard ability {standard_ability} "
    "and hidden ability {hidden_ability}. It plays the following roles: {roles}. "
    "It has a base experience of {base_experience}, stands {height} meters tall, and weighs {weight} kilograms."
)


all_pokemon_descriptions = []

for idx, entry in enumerate(data):
    name = entry["pokemon_species"].capitalize()
    base_experience = entry["base_experience"]
    height = round(entry["pokemon_height"] / 10, 1)  # decimeters → meters
    weight = round(entry["pokemon_weight"] / 10, 1)  # hectograms → kilograms

    pokemon_type = format_list(capitalize_list(entry["types"]))
    roles = format_list(capitalize_list(entry.get("role_type", []))) or "none"

    abilities = entry["abilities"]
    standard_abilities = [key for key, val in abilities.items() if val]
    hidden_abilities = [key for key, val in abilities.items() if not val]

    standard_ability = format_list(capitalize_list(standard_abilities)) or "None"
    hidden_ability = format_list(capitalize_list(hidden_abilities)) or "None"

    p_description = description_template.format(
        name=name,
        pokemon_type=pokemon_type,
        hidden_ability=hidden_ability,
        standard_ability=standard_ability,
        roles=roles,
        base_experience=base_experience,
        height=height,
        weight=weight,
    )

    all_pokemon_descriptions.append(p_description)


with open("/Users/yashvardhan/Documents/Desktop_Folders/ProjectsAndTutorials/pokebase/backend/all_pokemon_descriptions.json", "w") as f:
    json.dump(all_pokemon_descriptions, f)
