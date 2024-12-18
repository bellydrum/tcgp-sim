import json
from cards.models import CardCategory


DATA_FILEPATH = "data/imports/card_categories.json"

def import_objects():
    """
    Import CardCategory objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create CardCategory records based on the gathered objects
    """
    print(f"""Importing CardCategory objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    CardCategory.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create CardCategory records based on the gathered objects
    CardCategory.objects.bulk_create([CardCategory(**object) for object in objects_to_import])