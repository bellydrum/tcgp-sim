from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from cards.models import *


@login_required
def index(request):
    cards = [i for i in Card.objects.all()]
    pokemon_cards = [i for i in Pokemon.objects.all()]
    trainer_cards = [i for i in Trainer.objects.all()]

    context = {
        # "card_list": cards[:3],
        "card_list": [i for i in pokemon_cards][:3],
        "pokemon_list": pokemon_cards[:3],
        "trainer_cards": trainer_cards[:3]
    }

    return render(request, "cards/index.html", context=context)