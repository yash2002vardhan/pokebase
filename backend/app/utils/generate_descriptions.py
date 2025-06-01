import json

def format_list(items):
    """Formats a list as a comma-separated string with proper grammar."""
    return ', '.join(items)

def capitalize_list(items):
    """Capitalizes the first letter of each item in a list."""
    return [item.capitalize() for item in items]

description_template = (
    "{name} is a {pokemon_type} type Pokémon with the standard ability {standard_ability} "
    "and hidden ability {hidden_ability}. It plays the following roles: {roles}. "
    "It has a base experience of {base_experience}, stands {height} meters tall, and weighs {weight} kilograms."
)


def generate_descriptions(pokemon_data: dict) -> str:
    name = pokemon_data["pokemon_species"].capitalize()
    base_experience = pokemon_data["base_experience"]
    height = round(pokemon_data["pokemon_height"] / 10, 1)  # decimeters → meters
    weight = round(pokemon_data["pokemon_weight"] / 10, 1)  # hectograms → kilograms

    pokemon_type = format_list(capitalize_list(pokemon_data["types"]))
    roles = format_list(capitalize_list(pokemon_data.get("role_type", []))) or "none"

    abilities = pokemon_data["abilities"]
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

    return p_description


"""
The above function has been used to generate all the pokemon descriptions from the parsed data. The below code has been commented out because it is used to only once to generate the descriptions.
"""

# with open("all_parsed_data.json", "r") as f:
#     data = json.load(f)

# all_pokemon_descriptions = []

# for idx, entry in enumerate(data):

#     p_description = generate_descriptions(entry)

#     all_pokemon_descriptions.append(p_description)


# with open("/Users/yashvardhan/Documents/Desktop_Folders/ProjectsAndTutorials/pokebase/backend/all_pokemon_descriptions_test.json", "w") as f:
#     json.dump(all_pokemon_descriptions, f)
