#! /usr/bin/env python3

import re
from pprint import pprint

from cards.enums import *
from cards.models import *
from scripts.webscraping.site_scrapers.formatting_tools.text_tools import standardize_string
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

        attack_data["name"] = standardize_string(name_string, no_spaces=True, lower=True)
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

    existing_illustrators = [{
        "name": i.name,
    } for i in Illustrator.objects.all()]
    existing_illustrator_names = [i["name"].lower() for i in existing_illustrators]
    new_illustrators = []
    

    formatted_pokemon = []
    formatted_supporters = []
    formatted_items = []

    for response_object in response_data:
        # validate the response_object's structure
        response_object_matches_expected_structure = all([i in response_object.keys() for i in example_response_object.keys()])

        if not response_object_matches_expected_structure:
            error_message = f"ptcgpocket_converter.format_response_object | Response object does not have all expected properties: {response_object}"

            raise Exception(error_message)

        # fix Misty type info bug
        if response_object.get("name") == "Misty":
            response_object["type"] = "Supporter"

        # populated by the rest of the loop
        formatted_card = {}

        # add name and name_display
        formatted_name_display = response_object.get("name").replace(" ex", " EX")
        formatted_card["name"] = standardize_string(response_object.get("name", ""), no_spaces=True, lower=True)
        formatted_card["name_display"] = formatted_name_display

        # add card_type and trainer_type
        card_type = None
        trainer_type = None
        if response_object.get("type") == CardTypes.POKEMON.label:
            card_type = CardTypes.POKEMON.value
            trainer_type = None
        elif response_object.get("type") == TrainerTypes.SUPPORTER.label:
            card_type = CardTypes.TRAINER.value
            trainer_type = TrainerTypes.SUPPORTER
        elif response_object.get("type") == TrainerTypes.ITEM.label:
            card_type = CardTypes.TRAINER.value
            trainer_type = TrainerTypes.ITEM
        formatted_card["card_type"] = card_type
        formatted_card["trainer_type"] = trainer_type

        # add rarity
        rarity = None
        for rarity_enum in Rarities:
            if response_object.get("rarity") == rarity_enum.label:
                rarity = rarity_enum.value
                break
        formatted_card["rarity"] = rarity

        # add illustrators
        response_object_illustrator: str = response_object.get("illustrator") if response_object.get("illustrator") else None
        illustrator_object = None
        if response_object_illustrator:
            if response_object_illustrator.lower() not in existing_illustrator_names:
                illustrator_object = {
                    "name": response_object_illustrator
                }
                existing_illustrators.append(illustrator_object)
                existing_illustrator_names.append(response_object_illustrator.lower())
                new_illustrators.append(illustrator_object)
        formatted_card["illustrators"] = [response_object_illustrator] if response_object_illustrator else []

        # add sets
        formatted_card["sets"] = [{
            "code": response_object.get("setId"),
            "number": int(response_object.get("number")),
            "set_number": response_object.get("id"),
            "dex": dex if dex else None
        } for dex in response_object.get("dex").split(",")]

        if response_object.get("type") == "Pokemon":
            # add effect (ability)
            formatted_card["effect"] = response_object.get("ability") if response_object.get("ability") else {}

            # add type
            formatted_card["type"] = response_object.get("color").lower()

            # add stage
            stage = None
            for stage_enum in Stages:
                if response_object.get("stage") == stage_enum.label:
                    stage = stage_enum.value
                    break
            formatted_card["stage"] = stage

            # add ex
            formatted_card["ex"] = standardize_string(response_object.get("name", "")).endswith("ex")

            # add hp
            formatted_card["hp"] = int(response_object.get("hp"))

            # add retreat_cost
            formatted_card["retreat_cost"] = int(response_object.get("retreat")) if response_object.get("retreat") is not None else 0

            # add attacks
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
            formatted_card["attacks"] = attack_objects

            # add weakness type
            weakness_type = response_object.get("weakness", "").lower() if type(response_object.get("weakness")) == str else None
            if weakness_type == "none":
                weakness_type = None
            formatted_card["weakness_type"] = weakness_type

            formatted_pokemon.append(formatted_card)
        # handle Supporter-specific properties
        elif response_object.get("type") == "Supporter":
            # add effect
            effect = response_object.get("text") if response_object.get("text") else {}
            formatted_effect = effect.replace(" ", " ")
            formatted_card["effect"] = formatted_effect
    
            formatted_supporters.append(formatted_card)
        # handle Item-specific properties
        elif response_object.get("type") == "Item":
            # add effect
            effect = response_object.get("text") if response_object.get("text") else {}
            formatted_effect = effect.replace(" ", " ")
            formatted_card["effect"] = formatted_effect

            formatted_items.append(formatted_card)

    return {
        "pokemon": formatted_pokemon,
        "supporters": formatted_supporters,
        "items": formatted_items,
        "attacks": existing_attacks,
        "illustrators": existing_illustrators,
    }