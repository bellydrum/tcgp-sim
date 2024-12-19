#! /usr/bin/env python3

import re
from pprint import pprint

from cards.enums import *
from cards.models import *
# from scripts.webscraping.site_scrapers.example_responses.pokemonzone_response import example_response_object


def format_response_data(response_data):
    return response_data