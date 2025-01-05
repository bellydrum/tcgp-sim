#! /usr/bin/env python3

import json
from pprint import pprint
import sys

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string, standardize_string


"""
{
    "name": "Surprise Attack",
    "pokemonAttackId": "PK_002780_ATK_01",
    "damage": 50,
    "isNoDamage": false,
    "damageSymbol": "UNSPECIFIED",
    "damageSymbolLabel": null,
    "attackCost": [
        "Psychic"
    ],
    "description": "Flip a coin. If tails, this attack does nothing."
}
"""

"""
    id = models.BigAutoField(primary_key=True)
    attack_id = models.CharField(max_length=512, blank=False, null=False)                                       # "PK_002780_ATK_01"
    name = models.CharField(max_length=200, blank=False, null=False)                                            # "surprise_attack"
    name_display = models.CharField(max_length=200, blank=False, null=True)                                     # "Surprise Attack"
    cost = models.JSONField(blank=False, null=True, verbose_name="attack_cost")                                 # '{"psychic": 1}'
    damage = models.IntegerField(blank=False, null=True)                                                        # 50 | None
    is_no_damage = models.BooleanField(null=True)                                                               # False
    damage_symbol = models.CharField(max_length=8, blank=False, null=True)                                      # "+"
    effect = models.JSONField(blank=False, null=True, verbose_name="attack_effect")                             # <function_name>
    description = models.CharField(max_length=512, blank=False, null=True)                               # "Flip a coin. If tails, this attack does nothing."
"""


def format_attacks(response_attacks):
    # make dict of unique attacks by attack_id
    attacks_id_map = {attack.get("attack_id"): attack for attack in sorted(response_attacks, key=lambda x: x.get("attack_id"))}

    formatted_attacks = []

    for attack_object in attacks_id_map.values():
        formatted_attacks.append(attack_object)

    return sorted(formatted_attacks, key=lambda x: x.get("attack_id"))