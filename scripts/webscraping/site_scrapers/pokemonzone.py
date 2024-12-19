#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone_converter import format_response_data


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
    # response_data = json.loads(response.content.decode("utf-8"))