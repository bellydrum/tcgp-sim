import json
from cards.models import CardIllustrator, Illustrator


DATA_FILEPATH = "data/imports/illustrators.json"

def import_objects():
    """
    Import Illustrator objects

    Process
        Step 1. Truncate the current database table
        Step 2. Gather objects from the data file
        Step 3. Bulk create Illustrator records based on the gathered objects
    """
    print(f"""Importing Illustrator objects from {DATA_FILEPATH}""")

    # STEP 1. Truncate the current database table
    CardIllustrator.objects.all().delete()
    Illustrator.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())
    
    # STEP 3. Bulk create Illustrator records based on the gathered objects
    Illustrator.objects.bulk_create([Illustrator(name=object) for object in objects_to_import])