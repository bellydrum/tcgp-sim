#! /usr/bin/env python3

import json
from pprint import pprint

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


def format_energy_types(formatted_pokemon_cards):
    all_energy_types = []

    for pokemon_card in formatted_pokemon_cards:
        pokemon_object = pokemon_card.get("pokemon_object")

        weakness_energy_types = pokemon_object.get("weakness_type")

        all_energy_types.append(weakness_energy_types)

        attack_energy_costs = []

        for attack_object in pokemon_object.get("attacks"):
            attack_energy_costs.extend(json.loads(attack_object.get("cost")).keys())

        all_energy_types.extend(attack_energy_costs)
    
    energy_types = sorted([i for i in list(set(all_energy_types)) if i.lower() != "unspecified"])

    return [{
        "name": standardize_string(energy),
        "name_display": energy
    } for energy in energy_types]