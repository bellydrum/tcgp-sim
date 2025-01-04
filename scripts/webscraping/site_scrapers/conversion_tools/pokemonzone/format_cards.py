#! /usr/bin/env python3

from pprint import pprint
import sys
from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_pokemon import format_pokemon_object
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_trainers import format_trainer_object
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


VALID_CARD_TYPES = ["pokemon", "trainer"]


def format_card(card_object):
    # capitalize EX
    if type(card_object.get("name")) == str and card_object.get("name").endswith(" ex"):
        card_object["name"] = card_object["name"].removesuffix(" ex") + " EX"

    formatted_card = {
        "active": True,
        "card_id": card_object.get("cardId"),                                                                           # "TR_10_000090_00"
        "card_pokemon_id": card_object.get("pokemon", {}).get("pokemonId") if card_object.get("pokemon") else None,     # "TR_10_000090_00" | None
        "card_trainer_id": card_object.get("trainer", {}).get("trainerId") if card_object.get("trainer") else None,     # "TR_10_000090_00" | None
        "card_type": None,                                                                                              # "pokemon" | "trainer"
        "character_id": card_object.get("characterId"),                                                                 # "PARSHEN"
        "collection_number": card_object.get("collectionNumber"),                                                       # 67
        "description": standardize_string(card_object.get("description")),                                              # ""
        "dust_cost": card_object.get("dust_cost"),                                                                      # 70
        "expansion": card_object.get("expansion", {}).get("expansionId"),                                               # "A1"
        "flavor_text": standardize_string(card_object.get("flavorText")),                                               # ""
        "is_promo": card_object.get("isPromotion"),                                                                     # False
        "is_serial": card_object.get("isSerial"),                                                                       # False
        "name": standardize_string(card_object.get("name"), no_spaces=True, lower=True),                                # "cloyster"
        "name_display": card_object.get("name"),                                                                        # "Cloyster"
        "pokedex_number": card_object.get("pokedexNumber"),                                                             # 267
        "promotion_name": card_object.get("promotionName"),                                                             # ""
        "rarity": card_object.get("rarity"),                                                                            # "U"
        "rules_description": standardize_string(card_object.get("rulesDescription")),                                   # ""
        "series_id": card_object.get("seriesId"),                                                                       # "A"
        "ability_ids": [],  # populated below
        "attack_ids": [],  # populated below
        "available_packs": [],  # populated below
        "illustrators": [],  # populated below
        "variants": [],  # populated below

        # only used for creation of Pokemon and Trainer objects; not saved to Card
        "pokemon_object": format_pokemon_object(card_object.get("pokemon")) if card_object.get("pokemon") else None,
        "trainer_object": format_trainer_object(card_object.get("trainer")) if card_object.get("trainer") else None,
    }

    # determine card_type - "pokemon" | "trainer"
    if card_object.get("pokemon"):
        formatted_card["card_type"] = "pokemon"
    elif card_object.get("trainer"):
        formatted_card["card_type"] = "trainer"

    if card_object.get("pokemon"):
        # get ability_ids
        for ability_object in formatted_card.get("pokemon_object").get("abilities"):
            formatted_card["ability_ids"].append(ability_object.get("ability_id"))
        # get attack_ids
        for attack_object in formatted_card.get("pokemon_object").get("attacks"):
            formatted_card["attack_ids"].append(attack_object.get("attack_id"))

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

        if formatted_card.get("card_type") not in VALID_CARD_TYPES:
            error_message = f"""pokemonzone_converter.format_response_cards | ERROR | Formatted card does not have a card_type of "pokemon" or "trainer": {formatted_card}"""

            raise Exception(error_message)

        if formatted_card["card_type"] == "pokemon":
            formatted_pokemon_cards.append(formatted_card)
        elif formatted_card["card_type"] == "trainer":
            formatted_trainer_cards.append(formatted_card)

    return formatted_pokemon_cards, formatted_trainer_cards