import json
from pprint import pprint
from cards.models import Card, Rarity


DATA_FILEPATH = "data/imports/rarities.json"

def import_objects():
    """
    Import Rarity objects
    """

    print(f"""Importing Rarity objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    Card.objects.all().delete()
    Rarity.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Save Rarity objects
    for rarity_object in objects_to_import:
        new_object = Rarity(
            rarity_id = rarity_object.get("rarity_id"),
            name = rarity_object.get("name"),
            name_display = rarity_object.get("name_display")
        )

        new_object.save()