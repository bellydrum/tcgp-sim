from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from battle.models import *
from cards.models import *


@login_required
@csrf_protect
def index(request):
    context = {}

    if request.method == "POST":
        current_user = User.objects.get(id=request.session.get("user_id"))

        player_deck = Card.objects.all().order_by("?")[:20]
        player_hand = player_deck[:5]

        new_player = Player(
            user_id=current_user,
            points=0,
            active_card = player_hand[0],
            bench_1_card = player_hand[1],
            bench_2_card = player_hand[2],
            bench_3_card = player_hand[3],
            hand_card_ids = player_hand[4:],
            draw_pile = player_deck[5:],
        )

        # TODO - this is just for testing.
        opponent_deck = Card.objects.all().order_by("?")[:20]
        opponent_hand = opponent_deck[:5]

        new_opponent = Player(
            user_id=current_user,
            points=0,
            active_card = opponent_hand[0],
            bench_1_card = opponent_hand[1],
            bench_2_card = opponent_hand[2],
            bench_3_card = opponent_hand[3],
            hand_card_ids = opponent_hand[4:],
            draw_pile = opponent_deck[5:],
        )

        print(f"\n{new_player.discard_pile}\n")
        print(f"\n{type(new_player.discard_pile)}\n")

        context = {
            "battle_active": request.method == "POST",
            "player": {
                "object": new_player,
                "username": request.session.get("username"),
                "deck": player_deck,
                "hand": player_deck[:5]
            },
            "opponent": {
                "object": new_opponent,
                "username": None,
                "deck": opponent_deck,
                "hand": opponent_deck[:5]
            }
        }

    return render(request, "battle/index.html", context=context)