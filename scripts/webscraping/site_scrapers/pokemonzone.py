#! /usr/bin/env python3

import json
import requests
from pprint import pprint

from cards.models import *
from scripts.webscraping.site_scrapers.conversion_tools.pokemonzone_converter import format_response_data


SOURCE_URL = "https://www.pokemon-zone.com/api/game/game-data/"