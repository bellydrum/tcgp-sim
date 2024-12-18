#! /usr/bin/env python3

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


def format_expansions(response_expansions):
    formatted_expansions = []

    for expansion_object in response_expansions:
        formatted_expansions.append({
            "expansion_id": expansion_object.get("expansionId"),
            "name": standardize_string(expansion_object.get("displayName")),
            "name_display": expansion_object.get("displayName"),
            "card_count": expansion_object.get("cardCount") if type(expansion_object.get("cardCount")) is str and expansion_object.get("cardCount").isnumeric() else None,
            "is_promo": expansion_object.get("isPromo"),
            "sort_number": expansion_object.get("sortOrderPriority")
        })

    return sorted(formatted_expansions, key=lambda x: x.get("sort_number"))