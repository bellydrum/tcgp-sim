import json
from pprint import pprint


def extract_pokemon_from_card_objects(formatted_pokemon_cards):
    pokemon_objects_id_map = {}

    for formatted_pokemon_object in formatted_pokemon_cards:
        if pokemon := formatted_pokemon_object.get("pokemon"):
            if card_id := pokemon.get("pokemonId"):
                pokemon_objects_id_map[card_id] = pokemon
            else:
                print(pokemon.keys())
    
    # for i in pokemon_objects_id_map:
    #     pprint(pokemon_objects_id_map[i])

    return formatted_pokemon_cards, None