#! /usr/bin/env python3

import json
from pprint import pprint
import sys

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


def format_abilities(response_abilities):
    abilities_id_map = {ability.get("ability_id"): ability for ability in sorted(response_abilities, key=lambda x: x.get("ability_id"))}

    formatted_abilities = []

    for ability_object in abilities_id_map.values():
        formatted_abilities.append(ability_object)

    return sorted(formatted_abilities, key=lambda x: x.get("ability_id"))