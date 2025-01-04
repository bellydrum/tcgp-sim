import json
from pprint import pprint
from cards.models import Ability, Card, CardAbility


ABILITIES_FILEPATH = "data/imports/abilities.json"
POKEMON_FILEPATH = "data/imports/cards/pokemon.json"

def import_objects():
    """
    Import CardAbility relationship objects
    """

    print(f"""Creating CardAbility relation objects...""")

    # STEP 1. Truncate the current database table
    CardAbility.objects.all().delete()

    # STEP 2. Gather Pokemon Card objects
    with open(POKEMON_FILEPATH, "r") as f:
        existing_pokemon_cards = json.loads(f.read())

    # STEP 3. Create Card Ability relationship objects
    for pokemon_card in existing_pokemon_cards:
        for ability_id in pokemon_card.get("ability_ids"):
            try:
                new_relation = CardAbility(
                    card = Card.objects.get(card_id=pokemon_card.get("card_id")),
                    ability = Ability.objects.get(ability_id=ability_id)
                )
            except Exception as e:
                pprint(str(e))
                if "it returned" in str(e):
                    print(f"{pokemon_card.get('name_display')}")

                continue

            try:
                new_relation.save()
            except Exception as e:
                pprint(str(e))