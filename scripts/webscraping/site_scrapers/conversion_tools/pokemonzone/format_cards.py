#! /usr/bin/env python3

import re
from pprint import pprint

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import remove_html_tags, standardize_string


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
    # capitalize EX
    if type(card_object.get("name")) == str and card_object.get("name").endswith(" ex"):
        card_object["name"] = card_object["name"].removesuffix(" ex") + " EX"

    formatted_card = {
        "active": True,
        "card_id": card_object.get("cardId"),                                           # "TR_10_000090_00"
        "card_type": None,                                                              # "pokemon" | "trainer"
        "character_id": card_object.get("characterId"),                                 # "PARSHEN"
        "collection_number": card_object.get("collectionNumber"),                       # 67
        "description": remove_html_tags(card_object.get("description")),                # ""
        "dust_cost": card_object.get("dust_cost"),                                      # 70
        "expansion": card_object.get("expansion", {}).get("expansionId"),               # "A1"
        "flavor_text": remove_html_tags(card_object.get("flavorText")),                 # ""
        "is_promo": card_object.get("isPromotion"),                                     # False
        "is_serial": card_object.get("isSerial"),                                       # False
        "name": standardize_string(card_object.get("name")),                            # "cloyster"
        "name_display": card_object.get("name"),                                        # "Cloyster"
        "pokedex_number": card_object.get("pokedexNumber"),                             # 267
        "pokemon": card_object.get("pokemon"),                                          # <Pokemon object> | None
        "promotion_name": card_object.get("promotionName"),                             # ""
        "rarity": card_object.get("rarity"),                                            # "U"
        "rules_description": remove_html_tags(card_object.get("rulesDescription")),     # ""
        "series_id": card_object.get("seriesId"),                                       # "A"
        "trainer": card_object.get("trainer"),                                          # <Trainer object> | None
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

    # get illustrators
    if card_object.get("illustratorNames"):
        for illustrator in card_object.get("illustratorNames"):
            formatted_card["illustrators"].append(illustrator)

    # get variants
    if card_object.get("variants"):
        for variant in card_object.get("variants"):
            formatted_card["variants"].append(variant.get("cardId"))

    return formatted_card


def format_cards(response_cards):
    formatted_pokemon_cards = []
    formatted_trainer_cards = []

    for card_object in response_cards:
        formatted_card = format_card(card_object)

        if formatted_card.get("card_type") not in ["pokemon", "trainer"]:
            error_message = f"""pokemonzone_converter.format_response_cards | ERROR | Formatted card does not have a card_type of "pokemon" or "trainer": {formatted_card}"""

            raise Exception(error_message)
        
        formatted_pokemon_cards.append(formatted_card) if formatted_card["card_type"] == "pokemon" else formatted_trainer_cards.append(formatted_card)

    return formatted_pokemon_cards, formatted_trainer_cards