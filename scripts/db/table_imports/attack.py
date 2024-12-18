import json
from pprint import pprint
from cards.models import Attack, CardAttack


DATA_FILEPATH = "data/imports/attacks.json"

def import_objects():
    """
    Import Attack objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create Attack records based on the gathered objects
    """
    print(f"""Importing Attack objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    CardAttack.objects.all().delete()
    Attack.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create Attack records based on the gathered objects
    # Attack.objects.bulk_create([Attack(**object) for object in objects_to_import])

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

    for attack_object in objects_to_import:
        new_object = Attack(
            attack_id = attack_object.get("attack_id"),
            name = attack_object.get("name"),
            name_display = attack_object.get("name_display"),
            cost = attack_object.get("cost"),
            damage = attack_object.get("damage"),
            is_no_damage = attack_object.get("is_no_damage"),
            attack_description = attack_object.get("attack_description")
        )

        new_object.save()