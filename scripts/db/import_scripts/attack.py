import json
from cards.models import Attack, PokemonAttack


DATA_FILEPATH = "data/imports/attacks/attacks.json"

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
    PokemonAttack.objects.all().delete()
    Attack.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create Attack records based on the gathered objects
    Attack.objects.bulk_create([Attack(**object) for object in objects_to_import])