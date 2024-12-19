import json
from django.db.utils import IntegrityError

from cards.models import *


DATA_FILEPATH = "data/imports/cards/pokemon.json"

def import_objects():
    """
    Import Pokemon objects
    
    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Loop over each Pokemon object and generate the records
            3a. Create and save a new Pokemon record
            3b. Create relational records associated with this Pokemon
    """
    print(f"""Importing Pokemon objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    Card.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Create each Pokemon record individually
    for object_to_import in objects_to_import:
        # STEP 3a. Create and save a new Pokemon record

        weakness_type_record = EnergyType.objects.get(name=object_to_import.get("weakness_type")) if object_to_import.get("weakness_type") else None

        try:
            new_object = Pokemon(
                # inherited Card properties
                name = object_to_import.get("name"),                                                            # eg. "bulbasaur"
                name_display = object_to_import.get("name_display"),                                            # eg. "Bulbasaur"
                # category = CardCategory.objects.get(name=object_to_import.get("category")),                   # eg. "pokemon"
                card_type = "P",
                trainer_type = None,
                effect = object_to_import.get("effect"),                                                        # eg. {}
                # rarity = rarity_record,                                                                         # eg. 0
                illustrator = object_to_import.get("illustrator"),                                              # eg. "Narumi Sato"
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

        # STEP 3b. Create relational (many-to-many) records associated with this Pokemon

        # create PokemonAttack relations
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