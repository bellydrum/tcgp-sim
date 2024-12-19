from django.db import models

from cards.enums import *


# abstract and parent models

class EnergyType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    name_display = models.CharField(max_length=64, blank=False, null=True)

class Set(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=32, unique=True, blank=False, null=False)
    name = models.CharField(max_length=128, unique=True, blank=False, null=False)

class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    card_id = models.CharField(max_length=200, blank=False, null=True)
    name = models.CharField(max_length=200)
    name_display = models.CharField(max_length=200, blank=False)
    card_type = models.CharField(max_length=1, choices=CardTypes.choices)
    trainer_type = models.CharField(max_length=1, null=True, choices=TrainerTypes.choices)
    effect = models.JSONField(blank=False, null=True, verbose_name="card_effect")
    rarity = models.CharField(max_length=32, null=True, choices=Rarities.choices)
    illustrator = models.CharField(max_length=200, unique=False, blank=False, null=True)
    stage = models.CharField(max_length=64, blank=False, null=True)

class Attack(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "damage", "cost"], name="unique_name_damage_cost")
        ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    name_display = models.CharField(max_length=200, blank=False, null=True)
    cost = models.JSONField(blank=False, null=True, verbose_name="attack_cost")
    damage = models.IntegerField(blank=False, null=True)
    effect = models.JSONField(blank=False, null=True, verbose_name="attack_effect")
    effect_description = models.CharField(max_length=512, blank=False, null=True)

# import destinations

class Pokemon(Card, models.Model):
    type = models.ForeignKey(EnergyType, on_delete=models.SET_NULL, blank=False, null=True)
    ex = models.BooleanField(blank=False, null=True)
    hp = models.IntegerField(blank=False, null=True)
    weakness_type = models.ForeignKey(EnergyType, on_delete=models.SET_NULL, blank=False, null=True, related_name="pokemon_weakness_type")
    retreat_cost = models.SmallIntegerField(blank=False, null=True)

# relational models (many-to-many)

class CardAttack(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "attack"], name="unique_card_attack")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="card_attack_cards")
    attack = models.ForeignKey(Attack, on_delete=models.RESTRICT, blank=False, null=False, related_name="card_attack_attacks")

class CardSet(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "set", "dex", "number"], name="unique_card_set_dex_number")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False)
    # "A1" - reference to the Set this card belongs to
    set = models.ForeignKey(Set, on_delete=models.RESTRICT, blank=False, null=False, related_name="card_set_set")
    # "1" - this card's number in this set
    number = models.CharField(max_length=8, blank=False, null=False)
    # "A1-001" - this card's unique ID in this set (comprised of set.code and number)
    set_number = models.CharField(max_length=200, blank=False, null=False)
    # "A1M" - reference to the sub Set this card belongs to
    dex = models.ForeignKey(Set, on_delete=models.RESTRICT, blank=False, null=True)


# A1
# model.number == 