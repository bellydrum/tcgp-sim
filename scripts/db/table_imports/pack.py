import json
import sys

from cards.models import Expansion, Pack


DATA_FILEPATH = "data/imports/packs.json"


def import_objects():
    Pack.objects.all().delete()

    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    for object_to_import in objects_to_import:

        try:
            expansion = Expansion.objects.get(expansion_id=object_to_import.get("expansion_id"))
        except Exception as e:
            expansion = None

        
        new_object = Pack(
            pack_id = object_to_import.get("pack_id"),
            name = object_to_import.get("name"),
            name_display = object_to_import.get("name_display"),
            expansion = expansion,
            sort_number = object_to_import.get("sort_number")
        )

        new_object.save()