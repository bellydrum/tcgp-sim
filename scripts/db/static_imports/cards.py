import requests

from cards.models import Card


def import_files():
    cards = Card.objects.all().order_by("card_id")

    cards_static_path = "cards/static"
    image_directory = "cards/images/cards"

    for card in cards:
        image_url = card.image_url

        if image_url:
            response = requests.get(image_url)

            if response.status_code == 200:
                image_path = f"{image_directory}/{card.card_id}.png"

                with open(f"{cards_static_path}/{image_path}", 'wb') as f:
                    f.write(response.content)
                
                card.image_path = image_path

                card.save()

        else:
            print(f"scripts.db.static_imports.cards.import_files | ERROR | Card object {card.id} does not have an image_url.")