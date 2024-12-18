import json
from cards.models import Rarity


DATA_FILEPATH = "data/imports/rarities.json"

def import_objects():
    """
    Import Rarity objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create Rarity records based on the gathered objects
    """
    print(f"""Importing Rarity objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    Rarity.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create Rarity records based on the gathered objects
    Rarity.objects.bulk_create([Rarity(**object) for object in objects_to_import])