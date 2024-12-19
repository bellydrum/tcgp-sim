import json
from django.db.utils import IntegrityError

from cards.models import *


DATA_FILEPATH = "data/imports/cards/pokemon.json"

def import_objects():
    """
    Import Pokemon objects
    
    Process
        Step 1. Gather objects from the data file
        Step 2. Loop over each Pokemon object and generate the records
            2a. Create and save a new Pokemon record
            2b. Create relational records associated with this Pokemon
    """
    print(f"""Importing Pokemon objects from {DATA_FILEPATH}""")

    # STEP 1. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 2. Create each Pokemon record individually
    for object_to_import in objects_to_import:
        # STEP 2a. Create and save a new Pokemon record

        weakness_type_record = EnergyType.objects.get(name=object_to_import.get("weakness_type")) if object_to_import.get("weakness_type") else None

        try:
            new_object = Pokemon(
                # inherited Card properties
                name = object_to_import.get("name"),                                                            # eg. "bulbasaur"
                name_display = object_to_import.get("name_display"),                                            # eg. "Bulbasaur"
                card_type = object_to_import.get("card_type"),                                                  # eg. "P"
                trainer_type = object_to_import.get("trainer_type"),                                            # eg. None
                effect = object_to_import.get("effect"),                                                        # eg. {}
                rarity = object_to_import.get("rarity"),                                                        # eg. "C"
                stage = object_to_import.get("stage"),                                                          # eg. "Basic"

                # Pokemon-specific properties
                type = EnergyType.objects.get(name=object_to_import.get("type")),                               # eg. "grass"
                ex = object_to_import.get("ex"),                                                                # eg. false
                hp = object_to_import.get("hp"),                                                                # eg. 70
                weakness_type = weakness_type_record,                                                           # eg. "fire"
                retreat_cost = object_to_import.get("retreat_cost")                                             # eg. 1
            )
        except Exception as e:
            print(str(e))
            print(object_to_import)
            print("----------------------")

            raise Exception(e)

        try:
            new_object.save()
        except IntegrityError as ie:
            print(f"""- ERROR: IntegrityError for Pokemon "{object_to_import.get('name')}": {str(ie).strip()}""")
            continue

        # STEP 2b. Create relational (many-to-many) records associated with this Pokemon

        # create CardAttack relations
        for attack in object_to_import.get("attacks"):
            try:
                new_attack_relationship = CardAttack(
                    card=Card.objects.get(id=new_object.id),
                    attack=Attack.objects.get(name=attack["name"])          # attack = "razor_leaf" (Attack.name)
                )

                new_attack_relationship.save()
            except Exception as e:
                print(str(e))
                print(object_to_import)

                raise Exception(e)

        # create CardSet relations
        for set in object_to_import.get("sets", []):
            dex_value = Set.objects.get(code=set.get("dex")) if set.get("dex") else None

            new_set_relationship = CardSet(
                card=new_object,
                set=Set.objects.get(code=set.get("code")),              # set["code"] == "A1" (Set.code)
                number=set.get("number"),                               # set["number"] = "1"
                set_number=set.get("set_number"),                       # set["set_number"] == "A1-001"
                dex=dex_value,                                          # set["dex"] == "A1M" (Set.code")
            )

            new_set_relationship.save()

        # create CardIllustrator relations
        for illustrator_name in object_to_import.get("illustrators"):
            try:
                new_illustrator_relationship = CardIllustrator(
                    card=new_object,
                    illustrator=Illustrator.objects.get(name=illustrator_name)
                )

                new_illustrator_relationship.save()
            except Exception as e:
                print(f"ERROR: {str(e)}")
                print(illustrator_name)