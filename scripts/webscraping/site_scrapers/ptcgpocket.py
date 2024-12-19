#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.ptcgpocket_converter import format_response_data


SOURCE_URL = "https://api.dotgg.gg/cgfw/getcards?game=pokepocket"


# gather existing local JSON data

with open("data/imports/card_categories.json", "r") as f:
    existing_card_categories = json.loads(f.read())

with open("data/imports/energy_types.json", "r") as f:
    existing_energy_types = json.loads(f.read())

with open("data/imports/sets.json", "r") as f:
    existing_sets = json.loads(f.read())

with open("data/imports/attacks.json", "r") as f:
    existing_attacks = json.loads(f.read())

with open("data/imports/cards/pokemon.json", "r") as f:
    existing_pokemon = json.loads(f.read())


def scrape():
    print(f"Pulling game data from ptcgpocket.gg.\n")

    response = requests.get(SOURCE_URL)

    response_data = json.loads(response.content.decode("utf-8"))

    formatted_response_data = format_response_data(response_data)

    attacks = formatted_response_data["attacks"]
    pokemon = formatted_response_data["pokemon"]

    with open("data/imports/attacks.json", "w") as f:
        f.write(json.dumps(attacks, indent=4, ensure_ascii=False))
    
    with open("data/imports/cards/pokemon.json", "w") as f:
        f.write(json.dumps(pokemon, indent=4, ensure_ascii=False))