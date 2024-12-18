import json
from pprint import pprint
from cards.models import Card, CardPack, Pack


CARDS_FILEPATH = "data/imports/cards.json"
PACKS_FILEPATH = "data/imports/packs.json"

def import_objects():
    """
    Import CardPack objects
    """

    print(f"""Creating CardPack relation objects...""")

    # STEP 1. Truncate the current database table
    CardPack.objects.all().delete()

    # STEP 2. Gather Card objects
    with open(CARDS_FILEPATH, "r") as f:
        existing_cards = json.loads(f.read())

    # STEP 3. Create Card Pack relationship objects
    for card in existing_cards:
        for pack_id in card.get("available_packs"):
            try:
                new_relation = CardPack(
                    card=Card.objects.get(card_id=card.get("card_id")),
                    pack=Pack.objects.get(pack_id=pack_id)
                )
            except Exception as e:
                pprint(str(e))

                continue

            try:
                new_relation.save()
            except Exception as e:
                pprint(str(e))