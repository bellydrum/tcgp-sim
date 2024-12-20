#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.check_for_updates import get_removed_and_new_card_ids
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_cards import format_cards
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_pokemon import extract_pokemon_from_card_objects
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_trainers import extract_trainers_from_card_objects


SOURCE_URL = "https://www.pokemon-zone.com/api/game/game-data/"


# gather existing local JSON data

with open("data/imports/cards.json", "r") as f:
    existing_cards = json.loads(f.read())

with open("data/imports/cards/pokemon.json", "r") as f:
    existing_pokemon = json.loads(f.read())

with open("data/imports/cards/trainers.json", "r") as f:
    existing_trainers = json.loads(f.read())

with open("data/imports/attacks.json", "r") as f:
    existing_attacks = json.loads(f.read())

with open("data/imports/expansions.json", "r") as f:
    existing_expansions = json.loads(f.read())

with open("data/imports/illustrators.json", "r") as f:
    existing_illustrators = json.loads(f.read())

with open("data/imports/packs.json", "r") as f:
    existing_packs = json.loads(f.read())


def scrape():
    print(f"Pulling game data from pokemonzone.com.\n")

    response = requests.get(SOURCE_URL)
    response_data = json.loads(response.content.decode("utf-8")).get("data")

    # card
    formatted_pokemon_cards, formatted_trainer_cards = format_cards(response_data.get("cards"))

    formatted_pokemon_cards, formatted_pokemon = extract_pokemon_from_card_objects(formatted_pokemon_cards)
    formatted_trainer_cards, formatted_trainers = extract_trainers_from_card_objects(formatted_trainer_cards)
 
    # pack
    """
    {
        "description": "An A series vol. 3 promo pack",         # str
        "displayName": "Promo Pack A Series Vol. 3",            # str
        "name": "Promo Pack A Series Vol. 3",                   # str
        "packId": "AP001_0030_00_000",                          # str                       UID
        "sku": {
            "expansion": { ... },                               # <Expansion object>
            "packSkuId": "PROMO-A_3",                           # str
        },
        "sortOrderPriority": 1,                                 # int
    }
    """
    response_packs = response_data.get("packs")

    # expansion
    """
    {
        "cardCount": "068",                                     # str
        "displayName": "Mythical Island",                       # str
        "expansionId": "A1a",                                   # str                       UID
        "isPromo": false,                                       # bool
        "name": "Mythical Island",                              # str
        "sortOrderPriority": 2,                                 # int
    }
    """
    response_expansions = response_data.get("expansions")

    # pack list
    """
    {
        "packId": "AP001_0020_00_000",                          # str
        "cardIds": [
            "PK_90_000030_00",                                  # str
            ...,
        ]
    }
    """
    response_pack_card_ids = response_data.get("packCardIds")


    removed_pokemon_card_ids, new_pokemon_card_ids = get_removed_and_new_card_ids(existing_pokemon, formatted_pokemon_cards)
    removed_trainer_card_ids, new_trainer_card_ids = get_removed_and_new_card_ids(existing_trainers, formatted_trainer_cards)


    """
    update existing data objects
    """

    """ UPDATE CARDS """

    # create map for accessing formatted cards - { "TR_90_000060_01": {...}, }
    existing_card_id_map = {card["card_id"]: card for card in existing_cards}
    incoming_card_id_map = {card["card_id"]: card for card in formatted_pokemon_cards + formatted_trainer_cards}

    # refresh existing card objects with the incoming card data
    for card_object in existing_cards:
        card_id = card_object.get("card_id")
        if updated_card_object := incoming_card_id_map.get(card_id):
            existing_card_id_map[card_id] = updated_card_object
    
    # deactivate existing cards objects not present in the incoming card data
    for card_id in removed_pokemon_card_ids + removed_trainer_card_ids:
        card_to_deactivate = existing_card_id_map.get(card_id)
        card_to_deactivate["active"] = False

        existing_card_id_map[card_id] = card_to_deactivate
    
    # add new card objects from the incoming card data
    for card_id in new_pokemon_card_ids + new_trainer_card_ids:
        existing_card_id_map[card_id] = incoming_card_id_map[card_id]

    updated_cards = list(existing_card_id_map.values())

    # finally, update the data file
    with open("data/imports/cards.json", "w") as f:
        f.write(json.dumps(updated_cards, indent=4))

    with open("data/imports/cards.json", "r") as f:
        cards_latest = json.loads(f.read())

    print(f"CARDS COUNT: {len(cards_latest)}")