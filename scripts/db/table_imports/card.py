import json
from pprint import pprint

from cards.enums import TrainerTypes
from cards.models import Card, EnergyType, Pokemon, Rarity, Trainer


DATA_FILEPATH = "data/imports/cards.json"


def import_objects():
    Card.objects.all().delete()

    with open(DATA_FILEPATH, "r") as f:
        objects_to_import = json.loads(f.read())

    for object_to_import in objects_to_import:
        if object_to_import.get("card_type") == "pokemon":

            pokemon_object = object_to_import.get("pokemon_object")

            retreat_cost_type = pokemon_object.get("retreat_cost_type")[0] if pokemon_object.get("retreat_cost_type") else None
            weakness_type = None if pokemon_object.get("weakness_type") == "UNSPECIFIED" else pokemon_object.get("weakness_type")

            try:
                rarity_object = Rarity.objects.get(rarity_id=object_to_import.get("rarity") if object_to_import.get("rarity") else None)
            except Exception as e:
                rarity_object = None

            try:
                new_object = Pokemon(
                    # Card (parent) model attributes
                    active = object_to_import.get("active"),
                    attack_ids = object_to_import.get("attack_ids"),
                    card_id = object_to_import.get("card_id"),
                    card_pokemon_id = object_to_import.get("card_pokemon_id"),
                    card_trainer_id = object_to_import.get("card_trainer_id"),
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
                    promotion_name = object_to_import.get("promotion_name"),
                    rarity = rarity_object,
                    rules_description = object_to_import.get("rules_description"),
                    series_id = object_to_import.get("series_id"),
                    # Pokemon model attributes
                    pokemon_id = pokemon_object.get("pokemon_id"),
                    stage_number = pokemon_object.get("stage_number"),
                    stage_name = pokemon_object.get("stage_name"),
                    hp = pokemon_object.get("hp"),
                    is_ex = pokemon_object.get("is_ex"),
                    previous_evolution = pokemon_object.get("previous_evolution"),
                    retreat_cost_number = pokemon_object.get("retreat_cost_number"),
                    retreat_cost_type = EnergyType.objects.get(name_display=retreat_cost_type) if retreat_cost_type is not None else retreat_cost_type,
                    weakness_type = EnergyType.objects.get(name_display=weakness_type) if weakness_type else None
                    # available_packs = None,                                           # create CardPack record                        Packs must exist
                    # illustrators = None,                                              # create CardIllustrator record                 Illustrators must exist
                )
            except Exception as e:
                error_message = f"scripts.db.table_imports.card.import_objects | An error occurred while creating a new Pokemon object:\n{str(e)}\n{object_to_import}"
                print(error_message)

                raise Exception(e)
        
            try:
                new_object.save()
            except Exception as e:
                error_message = f"scripts.db.table_imports.card.import_objects | An error occurred while saving a new Pokemon object:\n{str(e)}\n{object_to_import}"
                print(error_message)

                raise Exception(e)
        
        elif object_to_import.get("card_type") == "trainer":
            trainer_object = object_to_import.get("trainer_object")

            trainer_type = None

            if type(trainer_object.get("trainer_type")) == str and trainer_object.get("trainer_type").lower() in [label.lower() for label in TrainerTypes.labels]:
                if trainer_object.get("trainer_type").lower() == "fossil":
                    trainer_type = TrainerTypes.FOSSIL
                elif trainer_object.get("trainer_type").lower() == "item":
                    trainer_type = TrainerTypes.ITEM
                elif trainer_object.get("trainer_type").lower() == "supporter":
                    trainer_type = TrainerTypes.SUPPORTER

            try:
                new_object = Trainer(
                    # Card (parent) model attributes
                    active = object_to_import.get("active"),
                    card_id = object_to_import.get("card_id"),
                    card_pokemon_id = object_to_import.get("card_pokemon_id"),
                    card_trainer_id = object_to_import.get("card_trainer_id"),
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
                    promotion_name = object_to_import.get("promotion_name"),
                    rarity = rarity_object,
                    rules_description = object_to_import.get("rules_description"),
                    series_id = object_to_import.get("series_id"),
                    # Trainer model attributes
                    trainer_id = trainer_object.get("trainer_id"),
                    trainer_type = trainer_type,
                    trainer_type_label = trainer_object.get("trainer_type")
                )
            except Exception as e:
                error_message = f"scripts.db.table_imports.card.import_objects | An error occurred while creating a new Trainer object:\n{str(e)}\n{object_to_import}"
                print(error_message)

                raise Exception(e)
        
            try:
                new_object.save()
            except Exception as e:
                error_message = f"scripts.db.table_imports.card.import_objects | An error occurred while saving a new Trainer object:\n{str(e)}\n{object_to_import}"
                print(error_message)

                raise Exception(e)