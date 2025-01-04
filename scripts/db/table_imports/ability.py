import json
from pprint import pprint
from cards.models import Ability


DATA_FILEPATH = "data/imports/abilities.json"

def import_objects():
    """
    Import Ability objects
    """
    print(f"""Importing Ability objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    Ability.objects.all()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    # STEP 3. Bulk create Attack records based on the gathered objects
    """
                "attack_id": attack_object.get("pokemonAttackId"),
                "name": standardize_string(attack_object.get("name")),
                "name_display": attack_object.get("name"),
                "cost": json.dumps(cost_dict),
                "damage": attack_object.get("damage"),
                "is_no_damage": attack_object.get("isNoDamage"),
                "damage_symbol": attack_object.get("damageSymbolLabel"),
                "effect": None,  # TODO - figure out how to reference attack effects.
                "attack_description": attack_object.get("description")
    """

    for ability_object in objects_to_import:
        new_object = Ability(
            ability_id = ability_object.get("ability_id"),
            name = ability_object.get("name"),
            name_display = ability_object.get("name_display"),
            description = ability_object.get("description"),
            effect = ability_object.get("effect")
        )

        new_object.save()