import json
from pprint import pprint
from cards.models import Card, CardIllustrator, Illustrator


CARDS_FILEPATH = "data/imports/cards.json"
ILLUSTRATORS_FILEPATH = "data/imports/illustrators.json"

def import_objects():
    """
    Import CardIllustrator objects
    """

    print(f"""Creating CardIllustrator relation objects...""")

    # STEP 1. Truncate the current database table
    CardIllustrator.objects.all().delete()

    # STEP 2. Gather objects from the data file
    with open(ILLUSTRATORS_FILEPATH, "r") as f:
        existing_card_illustrators = json.loads(f.read())
    
    # STEP 3. Gather Card objects
    with open(CARDS_FILEPATH, "r") as f:
        existing_cards = json.loads(f.read())
    
    card_illustrators = []

    for card in existing_cards:
        for name in card.get("illustrators"):
            card_illustrators.append(name)
    
    card_illustrators = sorted(list(set(card_illustrators)))


    if not card_illustrators == existing_card_illustrators:
        error_message = f"scripts.db.table_imports.card_illustrator.import_objects | The list of illustrators in data/illustrators.json does not match the illustrators on the card objects in data/cards.json. Illustrators:\n{existing_card_illustrators}\nCard illustrators:\n{card_illustrators}"
        print(error_message)

        raise Exception(error_message)

    for card in existing_cards:
        for illustrator in card.get("illustrators"):
            try:
                new_relation = CardIllustrator(
                    card=Card.objects.get(card_id=card.get("card_id")),
                    illustrator=Illustrator.objects.get(name=illustrator)
                )
            except Exception as e:
                pprint(str(e))

                continue

            try:
                new_relation.save()
            except Exception as e:
                pprint(str(e))