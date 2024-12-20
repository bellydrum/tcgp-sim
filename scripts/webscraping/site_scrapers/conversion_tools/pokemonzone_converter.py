#! /usr/bin/env python3

import re
from pprint import pprint

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string


"""
trainer: {
    'characterId': 'SAKAKI',
    'description': 'During this turn, attacks used by your Pokémon do +10 damage to your opponent’s Active Pokémon.',
    'name': 'Giovanni',
    'trainerId': 'TR_000150',
    'trainerType': 'Supporter',
    'trainerTypeLabel': 'Supporter'
}
"""

"""
pokemon: {
    "characterId": "MEW",
    "evolutionLabel": "Basic",
    "evolutionStage": "Basic",
    "evolutionStageNumber": "Basic",
    "hp": 60,
    "isEx": False,
    "name": "Mew",
    "pokemonAbilities": [ {...}, ],
    "pokemonAttacks": [ {...}, ],
    "pokemonId": "PK_002140",
    "pokemonTypes": ["Psychic"],
    "previousEvolution": None,
    "retreatAmount": 1,
    "retreatEnergyList": ["Colorless"],
    "weaknessType": "Darkness",
}
"""

"""
pokemonAttack: {
    "attackCost": ["Psychic"],
    "damage": 20,
    "damageSymbol": "UNSPECIFIED",
    "damageSymbolLabel": None,
    "description": "Your opponent reveals their hand.",
    "isNoDamage": False,
    "name": "Psy Report",
    "pokemonAttackId": "PK_002140_ATK_01"
}
"""

def format_card(card_object):
    formatted_card = {
        "available_packs": [],
        "illustrators": [],
        "variants": []
    }

    # determine card_type - "pokemon" | "trainer"
    if card_object.get("pokemon"):
        formatted_card["card_type"] = "pokemon"
    elif card_object.get("trainer"):
        formatted_card["card_type"] = "trainer"

    # get available_packs - ["AN001_0010_00_000"]
    if card_object.get("availablePacks"):
        for pack in card_object.get("availablePacks"):
            formatted_card["available_packs"].append(pack.get("packId"))

    # get card_id - "TR_10_000090_00"
    formatted_card["card_id"] = card_object.get("cardId")

    # get character_id - "PARSHEN"
    formatted_card["character_id"] = card_object.get("characterId")

    # get collection_number - 67
    formatted_card["collection_number"] = card_object.get("collectionNumber")

    # get description - ""
    formatted_card["description"] = card_object.get("description")

    # get dust_cost - 70
    formatted_card["dust_cost"] = card_object.get("dust_cost")

    # get expansion - "A1"
    formatted_card["expansion"] = card_object.get("expansion", {}).get("expansionId")

    # get flavor_text
    formatted_card["flavor_text"] = card_object.get("flavorText")

    # get illustrators
    if card_object.get("illustratorNames"):
        for illustrator in card_object.get("illustratorNames"):
            formatted_card["illustrators"].append(illustrator)

    # get is_promotion
    formatted_card["is_promo"] = card_object.get("isPromotion")

    # get is_serial
    formatted_card["is_serial"] = card_object.get("isSerial")

    # get name
    formatted_card["name"] = standardize_string(card_object.get("name"))

    # get name_display
    formatted_card["name_display"] = card_object.get("name")

    # get pokedex_number
    formatted_card["pokedex_number"] = card_object.get("pokedexNumber")

    # get pokemon
    formatted_card["pokemon"] = card_object.get("pokemon")

    # get promotion_name
    formatted_card["promotion_name"] = card_object.get("promotionName")

    # get rarity
    formatted_card["rarity"] = card_object.get("rarity")

    # get rules_description
    formatted_card["rules_description"] = card_object.get("rulesDescription")

    # get series_id
    formatted_card["series_id"] = card_object.get("seriesId")

    # get trainer
    formatted_card["trainer"] = card_object.get("trainer")

    # get variants
    if card_object.get("variants"):
        for variant in card_object.get("variants"):
            formatted_card["variants"].append(variant.get("cardId"))

    return formatted_card


def format_response_cards(response_cards):
    # view incoming card structure
    # pprint(response_cards[0])

    formatted_pokemon_cards = []
    formatted_trainer_cards = []

    for card_object in response_cards:
        formatted_card = format_card(card_object)

        if formatted_card.get("card_type") not in ["pokemon", "trainer"]:
            error_message = f"""pokemonzone_converter.format_response_cards | ERROR | Formatted card does not have a card_type of "pokemon" or "trainer": {formatted_card}"""

            raise Exception(error_message)
        
        formatted_pokemon_cards.append(formatted_card) if formatted_card["card_type"] == "pokemon" else formatted_trainer_cards.append(formatted_card)

    # view outgoing card structure
    print("\n")
    pprint(formatted_pokemon_cards[0])

    return {
        "pokemon": formatted_pokemon_cards,
        "trainers": formatted_trainer_cards
    }