#! /usr/bin/env python3

import re
from pprint import pprint

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.example_responses.ptcgpocket_response import example_response_object


ATTACK_STRING_REGEX = r"^({\w*} )([\w\s][^\d]*)([\w\d\+]*)$"  # "{GC} Powerful Bloom 50x"

ELEMENT_TYPE_MAP = {
    "C": "colorless",
    "M": "metal",
    "D": "darkness",
    "F": "fighting",
    "R": "fire",
    "G": "grass",
    "L": "lightning",
    "P": "psychic",
    "W": "water"
}


def standardize_string(string):
    return string.replace(" ", "_").lower() if string else ""


def parse_attack_string(attack_string):
    info = attack_string.get("info")
    effect = attack_string.get("effect")

    attack_data = {}

    attack_info_match = re.match(ATTACK_STRING_REGEX, info)
    if attack_info_match is not None:
        cost_string = attack_info_match.group(1)
        name_string = attack_info_match.group(2).strip() if attack_info_match.group(2) else ""
        damage = attack_info_match.group(3) if attack_info_match.group(3) else None

        if type(damage) == str:
            damage = damage.removesuffix("x").removesuffix("+")

        cost = {}

        for char in cost_string.strip("{}"):
            if char in ELEMENT_TYPE_MAP:
                if ELEMENT_TYPE_MAP[char] in cost:
                    cost[ELEMENT_TYPE_MAP[char]] += 1
                else:
                    cost[ELEMENT_TYPE_MAP[char]] = 1

        attack_data["name"] = standardize_string(name_string)
        attack_data["name_display"] = name_string
        attack_data["cost"] = cost
        attack_data["damage"] = damage
        attack_data["effect"] = {
            "action": None,
            "amount": None,
            "type": None,
            "description": effect
        }
        # TODO - remove <html></html> tags from effect via regex match
        attack_data["effect_description"] = effect

    return attack_data


def format_response_data(response_data):
    existing_attacks = [{
        "name": i.name,
        "name_display": i.name_display,
        "cost": i.cost,
        "damage": i.damage,
        "effect": i.effect
    } for i in Attack.objects.all()]
    existing_attack_names = [i["name"] for i in existing_attacks]
    new_attacks = []

    formatted_pokemon = []

    for response_object in response_data:
        # fix Misty type bug
        if response_object.get("name") == "Misty":
            response_object["type"] = "Supporter"

        if response_object.get("type") == "Pokemon":
            response_object_matches_expected_structure = all([i in response_object.keys() for i in example_response_object.keys()])

            if not response_object_matches_expected_structure:
                error_message = f"ptcgpocket_converter.format_response_object | Response object does not have all expected properties: {response_object}"

                raise Exception(error_message)

            # check to see if this object's Attacks exist locally
            response_object_attacks: str = response_object.get("attack", [])

            attack_objects = []

            if response_object_attacks:
                for response_object_attack in response_object_attacks:
                    attack_object = parse_attack_string(response_object_attack)
                    attack_objects.append(attack_object)

                    if attack_object["name"] not in existing_attack_names:
                        existing_attacks.append(attack_object)
                        existing_attack_names.append(attack_object["name"])
                        new_attacks.append(attack_object)
            
            # determine weakness_type
            
            weakness_type = response_object.get("weakness", "").lower() if type(response_object.get("weakness")) == str else None
            if weakness_type == "none":
                weakness_type = None

            # format name_display to capitalize any "ex"

            formatted_name_display = response_object.get("name")
            formatted_name_display = formatted_name_display.replace(" ex", " EX")

            rarity = None
            for rarity_enum in Rarities:
                if response_object.get("rarity") == rarity_enum.label:
                    rarity = rarity_enum.value
                    break

            # determine card_type and trainer_type

            if response_object.get("type").lower() in ["item", "supporter"]:
                card_type = CardTypes.TRAINER
                trainer_type = TrainerTypes.ITEM if response_object.get("type") == "item" else TrainerTypes.SUPPORTER
            elif response_object.get("type").lower() == "pokemon":
                card_type = CardTypes.POKEMON
                trainer_type = None
            else:
                card_type = None
                trainer_type = None

            formatted_pokemon.append({
                "name": standardize_string(response_object.get("name", "")),
                "name_display": formatted_name_display,
                "card_type": card_type,
                "trainer_type": trainer_type,
                "effect": response_object.get("ability") if response_object.get("effect") else {},
                "rarity": rarity,
                "illustrator": response_object.get("illustrator"),
                "type": response_object.get("color").lower(),
                "ex": standardize_string(response_object.get("name", "")).endswith("ex"),
                "stage": response_object.get("stage"),
                "hp": int(response_object.get("hp")),
                "weakness_type": weakness_type,
                "retreat_cost": int(response_object.get("retreat")) if response_object.get("retreat") is not None else 0,
                "attacks": attack_objects,
                "sets": [
                    {
                        "code": response_object.get("setId"),
                        "number": int(response_object.get("number")),
                        "set_number": response_object.get("id"),
                        "dex": dex
                    } for dex in response_object.get("dex").split(",")
                ]
            })
        elif response_object.get("type") == "Supporter":
            print(f"""Skipping card '{response_object.get("name")}' of card_type '{response_object.get("type")}'.""")
            pass
        elif response_object.get("type") == "Item":
            print(f"""Skipping card '{response_object.get("name")}' of card_type '{response_object.get("type")}'.""")
            pass

    return {
        "pokemon": formatted_pokemon,
        "attacks": existing_attacks,
    }