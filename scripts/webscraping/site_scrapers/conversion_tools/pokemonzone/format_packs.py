#! /usr/bin/env python3

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


def format_packs(response_packs):
    formatted_packs = []

    for pack_object in response_packs:
        formatted_packs.append({
            "pack_id": pack_object.get("packId"),
            "name": standardize_string(pack_object.get("displayName")),
            "name_display": pack_object.get("displayName"),
            "expansion_id": pack_object.get("sku", {}).get("expansion", {}).get("expansionId"),
            "sort_number": pack_object.get("sortOrderPriority")
        })

    return sorted(formatted_packs, key=lambda x: x.get("sort_number"))