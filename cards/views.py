from django.http import HttpResponse
from django.shortcuts import render

from cards.models import *


def index(request):
    cards = Card.objects.all()

    context = {
        "cards_list": cards
    }

    print(cards)

    context = {
        "card_records": [
            {
                "card": card,
                "card_set": card.cardset_set.filter(card=card)[0],
            } for card in cards
        ]
    }

    return render(request, "cards/index.html", context)