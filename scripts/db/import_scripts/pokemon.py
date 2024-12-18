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
    Card.objects.filter(category__name="pokemon").delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Create each Pokemon record individually
    for object_to_import in objects_to_import:

        # STEP 3a. Create and save a new Pokemon record
        new_object = Pokemon(
            # inherited Card properties
            name = object_to_import.get("name"),                                                            # eg. "bulbasaur"
            name_display = object_to_import.get("name_display"),                                            # eg. "Bulbasaur"
            category = CardCategory.objects.get(name=object_to_import.get("category")),                     # eg. "pokemon"
            effect = object_to_import.get("effect"),                                                        # eg. {}
            rarity = Rarity.objects.get(code=object_to_import.get("rarity")),                               # eg. 0
            illustrator = object_to_import.get("illustrator"),                                              # eg. "Narumi Sato"

            # Pokemon-specific properties
            type = EnergyType.objects.get(name=object_to_import.get("type")),                               # eg. "grass"
            ex = object_to_import.get("ex"),                                                                # eg. false
            stage = object_to_import.get("stage"),                                                          # eg. 0
            hp = object_to_import.get("hp"),                                                                # eg. 70
            weakness_type = EnergyType.objects.get(name=object_to_import.get("weakness_type")),             # eg. "fire"
            weakness_amount = object_to_import.get("weakness_amount"),                                      # eg. 20
            retreat_cost = object_to_import.get("retreat_cost")                                             # eg. 1
        )

        try:
            new_object.save()
        except IntegrityError as ie:
            print(f"""- ERROR: IntegrityError for Pokemon "{object_to_import.get('name')}": {str(ie).strip()}""")
            continue

        # STEP 3b. Create relational (many-to-many) records associated with this Pokemon

        # create PokemonAttack relations
        for attack in object_to_import.get("attacks"):
            new_attack_relationship = PokemonAttack(
                pokemon=new_object,
                attack=Attack.objects.get(name=attack)          # attack = "razor_leaf" (Attack.name)
            )

            new_attack_relationship.save()

        # create CardSet relations
        for set in object_to_import.get("sets", []):
            new_set_relationship = CardSet(
                card=new_object,
                set=Set.objects.get(code=set.get("code")),      # set["code"] == "A1" (Set.code)
                number=set.get("number"),                       # set["number"] = "1"
                set_number=set.get("set_number"),               # set["set_number"] == "A1-001"
                dex=Set.objects.get(code=set.get("dex")),       # set["dex"] == "A1M" (Set.code")
            )

            new_set_relationship.save()