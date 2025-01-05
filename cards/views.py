from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from cards.models import *


@login_required
def index(request):
    cards = Card.objects.all()
    pokemon_cards = [i for i in Pokemon.objects.all()]
    trainer_cards = [i for i in Trainer.objects.all()]

    context = {
        "show_card_images": True,
        "card_list": cards,
        "pokemon_list": pokemon_cards,
        "trainer_cards": trainer_cards
    }

    return render(request, "cards/index.html", context=context)