#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone_converter import format_response_cards


SOURCE_URL = "https://www.pokemon-zone.com/api/game/game-data/"


# gather existing local JSON data

with open("data/imports/cards/items.json", "r") as f:
    existing_items = json.loads(f.read())

with open("data/imports/cards/pokemon.json", "r") as f:
    existing_pokemon = json.loads(f.read())

with open("data/imports/cards/supporters.json", "r") as f:
    existing_supporters = json.loads(f.read())

with open("data/imports/attacks.json", "r") as f:
    existing_attacks = json.loads(f.read())

with open("data/imports/illustrators.json", "r") as f:
    existing_illustrators = json.loads(f.read())

with open("data/imports/sets.json", "r") as f:
    existing_sets = json.loads(f.read())


def scrape():
    print(f"Pulling game data from pokemonzone.com.\n")

    response = requests.get(SOURCE_URL)
    response_data = json.loads(response.content.decode("utf-8")).get("data")

    # card
    """
    {
        "availablePacks": [{...},],                             # list[ <Pack object> ]
        "cardId": "TR_10_000090_00",                            # str                       UID
        "characterId": "KOURANOKASEKI",                         # str
        "collectionNumber": 217,                                # int
        "description": "Play this card as if...",               # str
        "dustCost": 35,                                         # int
        "expansion: {...},                                      # <Expansion object>
        "flavorText": "Cloyster that live in seas...",          # str | None
        "illustratorNames": [str,],                             # list[ str ]
        "isInAllExpansionPacks": False,                         # bool
        "isPromotion": False,                                   # bool
        "isSerial": False,                                      # bool
        "name": "Cloyster",                                     # str
        "pokedexNumber": 91,                                    # int
        "pokemon": {...},                                       # None | <Pokemon object>
        "promotionCardSource": "Obtained from a promo pack",    # str | None
        "promotionName": "PROMO-A",                             # str | None
        "rarity": "U",                                          # str
        "rulesDescription": "You may play any number...",       # str | None
        "seriesId": "A",                                        # str
        "trainer": None,                                        # None | <Trainer object>
    }
    """
    formatted_response_cards = format_response_cards(response_data.get("cards"))
    formatted_pokemon_cards = formatted_response_cards["pokemon"]
    formatted_trainer_cards = formatted_response_cards["trainers"]

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