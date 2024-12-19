import json
from django.db.utils import IntegrityError

from cards.models import *


DATA_FILEPATH = "data/imports/cards/items.json"

def import_objects():
    """
    Import Item objects
    
    Process
        Step 1. Gather objects from the data file
        Step 2. Loop over each Item object and generate the records
            2a. Create and save a new Item record
            2b. Create relational records associated with this Item
    """
    print(f"""Importing Item objects from {DATA_FILEPATH}""")

    # STEP 1. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    # STEP 2. Create each Item record individually
    for object_to_import in objects_to_import:
        # STEP 2a. Create and save a new Item record

        try:
            new_object = Item(
                # inherited Card properties
                name = object_to_import.get("name"),                                                            # eg. "misty"
                name_display = object_to_import.get("name_display"),                                            # eg. "Misty"
                card_type = object_to_import.get("card_type"),                                                  # eg. "T"
                trainer_type = object_to_import.get("trainer_type"),                                            # eg. "S"
                effect = object_to_import.get("effect"),                                                        # eg. {}
                rarity = object_to_import.get("rarity"),                                                        # eg. "C"
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

        # STEP 2b. Create relational (many-to-many) records associated with this Item

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