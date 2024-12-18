#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.ptcgpocket_converter import format_response_data


SOURCE_URL = "https://api.dotgg.gg/cgfw/getcards?game=pokepocket"


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

def cards_match(card_1, card_2):
    # check the name
    if card_1.get("name") != card_2.get("name"):
        return False

    # if the names match, check the rarity
    if card_1.get("rarity") != card_2.get("rarity"):
        return False
    
    # if the name and rarity match, check the sets
    card_1_sets = card_1.get("sets")
    card_2_sets = card_2.get("sets")

    # return True if both sets are None or []
    if card_1_sets == card_2_sets:
        return True
    
    if type(card_1_sets) == list and type(card_2_sets) == list:
        # return False if the number of sets does not match
        if len(card_1_sets) != len(card_2_sets):
            return False
        
        card_1_set_numbers = [card_set["number"] for card_set in card_1_sets]
        card_2_set_numbers = [card_set["number"] for card_set in card_2_sets]

        # return True or False for whether the card set numbers match
        return sorted(card_1_set_numbers) == sorted(card_2_set_numbers)
    else:
        error_message = f"ptcgpocket.cards_match | One of the two cards has an invalid set list:\n{card_1}\n{card_2}"

        raise Exception(error_message)


def get_new_cards(existing_batch, latest_batch):
    new_cards = []

    for current_card in latest_batch:
        card_is_new = False

        if existing_card_matches := [i for i in filter(lambda x: x["name"] == current_card["name"], existing_batch)]:
            match_found = False

            for existing_card_match in existing_card_matches:
                if cards_match(existing_card_match, current_card):
                    match_found = True

                    break

            if not match_found:
                card_is_new = True
        else:
            card_is_new = True

        if card_is_new:
            print(f"--- Found a new {current_card['name_display']}!")

            new_cards.append(current_card)
    
    return new_cards


def scrape():
    print(f"Pulling game data from ptcgpocket.gg.\n")

    response = requests.get(SOURCE_URL)
    response_data = json.loads(response.content.decode("utf-8"))

    formatted_response_data = format_response_data(response_data)

    items = formatted_response_data["items"]
    pokemon = formatted_response_data["pokemon"]
    supporters = formatted_response_data["supporters"]
    attacks = formatted_response_data["attacks"]
    illustrators = formatted_response_data["illustrators"]
    # sets = []

    new_items = get_new_cards(existing_items, items)
    new_pokemon = get_new_cards(existing_pokemon, pokemon)
    new_supporters = get_new_cards(existing_supporters, supporters)

    items.extend(new_items)
    pokemon.extend(new_pokemon)
    supporters.extend(new_supporters)

    with open("data/imports/attacks.json", "w") as f:
        f.write(json.dumps(attacks, indent=4, ensure_ascii=False))

    with open("data/imports/illustrators.json", "w") as f:
        f.write(json.dumps(illustrators, indent=4, ensure_ascii=False))

    with open("data/imports/cards/pokemon.json", "w") as f:
        f.write(json.dumps(pokemon, indent=4, ensure_ascii=False))

    with open("data/imports/cards/supporters.json", "w") as f:
        f.write(json.dumps(supporters, indent=4, ensure_ascii=False))

    with open("data/imports/cards/items.json", "w") as f:
        f.write(json.dumps(items, indent=4, ensure_ascii=False))