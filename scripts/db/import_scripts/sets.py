import json
from cards.models import CardSet, Set


DATA_FILEPATH = "data/imports/sets.json"

def import_objects():
    """
    Import Set objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create Set records based on the gathered objects
    """
    print(f"""Importing Set objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    CardSet.objects.all().delete()
    Set.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create Set records based on the gathered objects
    Set.objects.bulk_create([Set(**object) for object in objects_to_import])