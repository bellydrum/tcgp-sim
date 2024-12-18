#! /usr/bin/env python3

import json
import os
import requests

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.check_for_updates import get_removed_and_new_card_ids
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_attacks import format_attacks
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_cards import format_cards
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_energy_types import format_energy_types
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_expansions import format_expansions
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone.format_packs import format_packs
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string


SOURCE_URL = os.environ.get("DATA_SOURCE_URL_POKEMONZONE")


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

    # rarities

    formatted_rarities = [{
        "rarity_id": i.get("id"),
        "name": standardize_string(i.get("name"), no_spaces=True, lower=True),
        "name_display": i.get("name")
    } for i in response_data.get("rarities")]

    with open(f"data/imports/rarities.json", "w") as f:
        f.write(json.dumps(formatted_rarities, indent=4))

    # cards

    formatted_pokemon_cards, formatted_trainer_cards = format_cards(response_data.get("cards"))


    # energy types

    formatted_energy_types = format_energy_types(formatted_pokemon_cards)

    with open(f"data/imports/energy_types.json", "w") as f:
        f.write(json.dumps(formatted_energy_types, indent=4))


    # packs

    response_packs = response_data.get("packs")
    formatted_packs = format_packs(response_packs)

    with open("data/imports/packs.json", "w") as f:
        f.write(json.dumps(formatted_packs, indent=4))


    # expansions

    response_expansions = response_data.get("expansions")
    formatted_expansions = format_expansions(response_expansions)

    with open("data/imports/expansions.json", "w") as f:
        f.write(json.dumps(formatted_expansions, indent=4))

    response_attacks = [attack for attacks in [card.get("pokemon_object").get("attacks") for card in formatted_pokemon_cards] for attack in attacks]
    formatted_attacks = format_attacks(response_attacks)

    with open("data/imports/attacks.json", "w") as f:
        f.write(json.dumps(formatted_attacks, indent=4))


    # distinguish removed cards from added cards

    removed_pokemon_card_ids, new_pokemon_card_ids = get_removed_and_new_card_ids(existing_pokemon, formatted_pokemon_cards)
    removed_trainer_card_ids, new_trainer_card_ids = get_removed_and_new_card_ids(existing_trainers, formatted_trainer_cards)


    """
    update existing data objects
    """

    """
    UPDATE CARDS DATA
    """

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

    updated_cards = sorted(list(existing_card_id_map.values()), key=lambda card: card.get("card_id"))

    updated_pokemon = [card for card in updated_cards if card.get("card_type") == "pokemon"]
    updated_trainers = [card for card in updated_cards if card.get("card_type") == "trainer"]

    # finally, update the data file
    with open("data/imports/cards.json", "w") as f:
        f.write(json.dumps(updated_cards, indent=4, ensure_ascii=False))

    with open("data/imports/cards.json", "r") as f:
        cards_latest = json.loads(f.read())

    print(f"CARDS COUNT: {len(cards_latest)}")

    with open("data/imports/cards/pokemon.json", "w") as f:
        f.write(json.dumps(updated_pokemon, indent=4, ensure_ascii=False))

    with open("data/imports/cards/trainers.json", "w") as f:
        f.write(json.dumps(updated_trainers, indent=4, ensure_ascii=False))


    """
    GATHER OTHER DATA FOR UPDATING
    """

    all_card_illustrators = []

    for card in updated_cards:
        [all_card_illustrators.append(name) for name in card.get("illustrators")]
    
    all_card_illustrators = sorted(list(set(all_card_illustrators)))

    with open("data/imports/illustrators.json", "w") as f:
        f.write(json.dumps(all_card_illustrators, indent=4))