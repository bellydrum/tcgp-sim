import json
import sys

from cards.models import Expansion


DATA_FILEPATH = "data/imports/expansions.json"


def import_objects():
    Expansion.objects.all().delete()

    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    for object_to_import in objects_to_import:
        try:
            new_object = Expansion(
                expansion_id = object_to_import.get("expansion_id"),
                name = object_to_import.get("name"),
                name_display = object_to_import.get("name_display"),
                card_count = object_to_import.get("card_count"),
                is_promo = object_to_import.get("is_promo"),
                sort_number = object_to_import.get("sort_number")
            )
        except Exception as e:
            print(str(e))
        
        try:
            new_object.save()
        except Exception as e:
            print(str(e))