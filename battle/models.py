from django.db import models
from django.contrib.auth.models import User

from account import models as account_models
from cards import models as cards_models


class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    in_matchmaking = models.BooleanField(blank=False, null=False, default=True)
    points = models.SmallIntegerField(blank=False, null=False, default=0)
    active_card = models.ForeignKey(cards_models.Card, on_delete=models.SET_NULL, blank=False, null=True, related_name="player_active_card")
    bench_1_card = models.ForeignKey(cards_models.Card, on_delete=models.SET_NULL, blank=False, null=True, related_name="player_bench_1_card")
    bench_2_card = models.ForeignKey(cards_models.Card, on_delete=models.SET_NULL, blank=False, null=True, related_name="player_bench_2_card")
    bench_3_card = models.ForeignKey(cards_models.Card, on_delete=models.SET_NULL, blank=False, null=True, related_name="player_bench_3_card")
    hand_card_ids = models.JSONField(blank=False, null=True)
    draw_pile = models.JSONField(blank=False, null=True)
    discard_pile = models.JSONField(blank=False, null=False, default=list)

class Battle(models.Model):
    id = models.BigAutoField(primary_key=True)
    battle_id = models.BigIntegerField(blank=False, null=True)
    active = models.BooleanField(blank=False, null=False, default=False)
    started = models.BooleanField(blank=False, null=False, default=False)
    completed = models.BooleanField(blank=False, null=False, default=False)
    player_1_id = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True, related_name="battle_player_1")
    player_2_id = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True, related_name="battle_player_2")
    starting_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True, related_name="battle_starting_player")
    winning_player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=True)

class PlayerDeck(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Player, on_delete=models.CASCADE, blank=False, null=False)
    card_ids = models.JSONField(blank=False, null=True)
    card_1 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_1")
    card_2 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_2")
    card_3 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_3")
    card_4 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_4")
    card_5 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_5")
    card_6 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_6")
    card_7 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_7")
    card_8 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_8")
    card_9 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_9")
    card_10 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_10")
    card_11 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_11")
    card_12 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_12")
    card_13 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_13")
    card_14 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_14")
    card_15 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_15")
    card_16 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_16")
    card_17 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_17")
    card_18 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_18")
    card_19 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_19")
    card_20 = models.ForeignKey(cards_models.Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="player_deck_card_20")