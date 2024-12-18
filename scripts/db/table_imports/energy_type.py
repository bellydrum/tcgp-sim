import json
from cards.models import EnergyType, Pokemon


DATA_FILEPATH = "data/imports/energy_types.json"

def import_objects():
    """
    Import EnergyType objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create EnergyType records based on the gathered objects
    """
    print(f"""Importing EnergyType objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    Pokemon.objects.all().delete()
    EnergyType.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create EnergyType records based on the gathered objects
    EnergyType.objects.bulk_create([EnergyType(**object) for object in objects_to_import])