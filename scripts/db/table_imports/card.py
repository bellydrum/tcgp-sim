import json

from cards.models import *
from scripts.db.table_imports.pokemon import import_objects as import_pokemon
from scripts.db.table_imports.trainer import import_objects as import_trainers


DATA_FILEPATH = "data/imports/cards.json"


def import_objects():
    Card.objects.all().delete()

    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    for object_to_import in objects_to_import:
        try:
            new_object = Card(
                active = object_to_import.get("active"),
                card_id = object_to_import.get("card_id"),
                card_type = object_to_import.get("card_type"),
                character_id = object_to_import.get("character_id"),
                collection_number = object_to_import.get("collection_number"),
                description = object_to_import.get("description"),
                dust_cost = object_to_import.get("dust_cost"),
                effect = object_to_import.get("effect"),
                expansion_id = object_to_import.get("expansion"),
                flavor_text = object_to_import.get("flavor_text"),
                is_promo = object_to_import.get("is_promo"),
                is_serial = object_to_import.get("is_serial"),
                name = object_to_import.get("name"),
                name_display = object_to_import.get("name_display"),
                pokedex_number = object_to_import.get("pokedex_number"),
                # pokemon = None,                                                   # None | reference Pokemon object               Pokemon must exist
                promotion_name = object_to_import.get("promotion_name"),
                rarity = object_to_import.get("rarity"),
                rules_description = object_to_import.get("rules_description"),
                series_id = object_to_import.get("series_id")
                # trainer = None,                                                   # None | reference Trainer object               Trainer must exist
                # available_packs = None,                                           # create CardPack record                        Packs must exist
                # illustrators = None,                                              # create CardIllustrator record                 Illustrators must exist
            )

        except Exception as e:
            error_message = f"scripts.db.table_imports.card.import_objects | An error occurred creating a new Card object:\n{str(e)}\n{object_to_import}"
            print(error_message)

            raise Exception(e)
        
        try:
            new_object.save()
        except Exception as e:
            error_message = f"scripts.db.table_imports.card.import_objects | An error occurred saving a new Card object:\n{str(e)}\n{object_to_import}"
            print(error_message)

            raise Exception(e)

    import_pokemon()
    import_trainers()