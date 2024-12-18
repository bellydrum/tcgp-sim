import json
from pprint import pprint
from cards.models import Attack, Card, CardAttack


ATTACKS_FILEPATH = "data/imports/attacks.json"
POKEMON_FILEPATH = "data/imports/cards/pokemon.json"

def import_objects():
    """
    Import CardAttack relationship objects
    """

    print(f"""Creating CardAttack relation objects...""")

    # STEP 1. Truncate the current database table
    CardAttack.objects.all().delete()

    # STEP 2. Gather Pokemon Card objects
    with open(POKEMON_FILEPATH, "r") as f:
        existing_pokemon_cards = json.loads(f.read())

    # STEP 3. Create Card Pack relationship objects
    for pokemon_card in existing_pokemon_cards:
        for attack_id in pokemon_card.get("attack_ids"):
            try:
                new_relation = CardAttack(
                    card = Card.objects.get(card_id=pokemon_card.get("card_id")),
                    attack = Attack.objects.get(attack_id=attack_id)
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