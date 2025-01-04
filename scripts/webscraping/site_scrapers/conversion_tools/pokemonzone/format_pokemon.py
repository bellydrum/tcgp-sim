import json
from pprint import pprint

from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string


def format_pokemon_object(pokemon_object):
    abilities = []
    attacks = []

    """
     'pokemonAbilities': [{'description': 'Once during your turn, if this Pokémon '
                                      'is in the Active Spot, you may make '
                                      'your opponent’s Active Pokémon '
                                      'Poisoned.',
                       'name': 'Gas Leak',
                       'pokemonAbilityId': 'PK_001770_ABL_01'}],
    """

    for ability_object in pokemon_object.get("pokemonAbilities"):
        abilities.append({
            "ability_id": ability_object.get("pokemonAbilityId"),
            "name": standardize_string(ability_object.get("name"), no_spaces=True, lower=True),
            "name_display": ability_object.get("name"),
            "description": standardize_string(ability_object.get("description")),
            "effect": None,  # TODO - figure out how to reference ability effects.
        })

    for attack_object in pokemon_object.get("pokemonAttacks"):
        cost_dict = {}

        cost_list = attack_object.get("attackCost")

        for energy_name in cost_list:
            if energy_name not in cost_dict.keys():
                cost_dict[energy_name] = 1
            else:
                cost_dict[energy_name] += 1

        attacks.append({
            "attack_id": attack_object.get("pokemonAttackId"),
            "name": standardize_string(attack_object.get("name"), no_spaces=True, lower=True),
            "name_display": attack_object.get("name"),
            "cost": json.dumps(cost_dict),
            "damage": attack_object.get("damage"),
            "is_no_damage": attack_object.get("isNoDamage"),
            "damage_symbol": attack_object.get("damageSymbolLabel"),
            "description": standardize_string(attack_object.get("description")),
            "effect": None,  # TODO - figure out how to reference attack effects.
        })

    return {
        "pokemon_id": pokemon_object.get("pokemonId"),
        "stage_number": pokemon_object.get("evolutionStageNumber"),
        "stage_name": pokemon_object.get("evolutionLabel"),
        "hp": pokemon_object.get("hp"),
        "is_ex": pokemon_object.get("isEx"),
        "previous_evolution": pokemon_object.get("previousEvolution", {}).get("pokemonId") if pokemon_object.get("previousEvolution") else None,
        "retreat_cost_number": pokemon_object.get("retreatAmount"),
        "retreat_cost_type": pokemon_object.get("retreatEnergyList"),
        "weakness_type": pokemon_object.get("weaknessType"),
        "attacks": attacks if attacks else [],
        "abilities": abilities if abilities else [],
    }

def extract_pokemon_from_card_objects(formatted_pokemon_cards):
    return formatted_pokemon_cards, [card.get("pokemon_object") for card in formatted_pokemon_cards]