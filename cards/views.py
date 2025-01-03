from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from cards.models import *


@login_required
def index(request):
    cards = Card.objects.all()

    context = {
        "cards_list": cards
    }

    print(cards)

    return render(request, "cards/index.html", context=context)