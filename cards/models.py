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

class Expansion(models.Model):
    id = models.BigAutoField(primary_key=True)
    expansion_id = models.CharField(max_length=64, blank=False, null=True)                                      # "A1", "A1a"
    name = models.CharField(max_length=512, blank=False, null=True)                                             # "genetic_apex"
    name_display = models.CharField(max_length=512, blank=False, null=True)                                     # "Genetic Apex"
    card_count = models.IntegerField(blank=False, null=True)                                                    # 226
    is_promo = models.BooleanField()                                                                            # False
    sort_order_priority = models.IntegerField(blank=False, null=True)                                           # 1

class Pack(models.Model):
    id = models.BigAutoField(primary_key=True)
    pack_id = models.CharField(max_length=64, blank=False, null=True)                                           # "A1", "A1a"
    name = models.CharField(max_length=512, blank=False, null=True)                                             # "mewtwo_pack"
    name_display = models.CharField(max_length=512, blank=False, null=True)                                     # "Mewtwo Pack"
    expansion = models.ForeignKey(Expansion, on_delete=models.RESTRICT, blank=False, null=True)

class Illustrator(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)

class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.BooleanField(blank=False, null=False, default=True)                                         # True
    card_id = models.CharField(max_length=200, blank=False, null=True)                                          # "PK_10_000670_00"
    card_pokemon_id = models.CharField(max_length=200, blank=False, null=True)
    card_trainer_id = models.CharField(max_length=200, blank=False, null=True)
    card_type = models.CharField(max_length=128, choices=CardTypes.choices)                                     # "pokemon"
    character_id = models.CharField(max_length=200, blank=False, null=True)                                     # "PARSHEN"
    collection_number = models.SmallIntegerField(blank=False, null=True)                                        # 67
    description = models.CharField(max_length=2048, blank=False, null=True)                                     # ""
    dust_cost = models.IntegerField(blank=False, null=True)                                                     # 70
    effect = models.JSONField(blank=False, null=True, verbose_name="card_effect")                               #
    expansion_id = models.CharField(max_length=64, blank=False, null=True)                                      # "A1"
    flavor_text = models.CharField(max_length=2048, blank=False, null=True)                                     # "Cloyster that live in seas..."
    is_promo = models.BooleanField(blank=False, null=True)                                                      # False
    is_serial = models.BooleanField(blank=False, null=True)                                                     # False
    name = models.CharField(max_length=200)                                                                     # "cloyster"
    name_display = models.CharField(max_length=200, blank=False)                                                # "Cloyster"
    pokedex_number = models.SmallIntegerField(blank=False, null=True)                                           # 91
    promotion_name = models.CharField(max_length=512, blank=False, null=True)                                   # None
    rarity = models.CharField(max_length=32, null=True, choices=Rarities.choices)                               # "U"
    rules_description = models.CharField(max_length=2048, blank=False, null=True)                               # "..."
    trainer_type = models.CharField(max_length=1, null=True, choices=TrainerTypes.choices)                      # None ("supporter", "item")
    series_id = models.CharField(max_length=8, blank=False, null=True)                                          # "A"
    variants = models.JSONField(blank=False, null=True, verbose_name="card_variants")                           # "['PK_10_000670_00', 'PK_10_000671_00']"

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

""" import destinations """

class Pokemon(Card, models.Model):
    stage_number = models.SmallIntegerField(blank=False, null=True)                                             # 1
    stage_name = models.CharField(max_length=16, null=True, choices=Stages.choices)                             # "Stage 1"
    hp = models.SmallIntegerField(blank=False, null=True)                                                       # 90
    is_ex = models.BooleanField(blank=False, null=True)                                                         # False
    pokemon_id = models.CharField(max_length=512, blank=False, null=False)                                      # "PK_000340"
    previous_evolution = models.CharField(max_length=512, blank=False, null=False)                              # "PK_000339"
    retreat_cost_number = models.SmallIntegerField(blank=False, null=True)                                      # 2
    retreat_cost_type = models.ForeignKey(EnergyType, on_delete=models.RESTRICT, blank=False, null=True, related_name="pokemon_retreat_cost_type")
    weakness_type = models.ForeignKey(EnergyType, on_delete=models.RESTRICT, blank=False, null=True, related_name="pokemon_weakness_type")

class Trainer(Card, models.Model):
    pass

#
# relational models (many-to-many)
#

class CardAttack(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "attack"], name="unique_card_attack")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="card_attack_cards")
    attack = models.ForeignKey(Attack, on_delete=models.RESTRICT, blank=False, null=False, related_name="card_attack_attacks")

class CardIllustrator(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "illustrator"], name="unique_card_illustrator")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False)
    illustrator = models.ForeignKey(Illustrator, on_delete=models.RESTRICT, blank=False, null=False)

class CardPack(models.Model):
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False)
    pack = models.ForeignKey(Pack, on_delete=models.RESTRICT, blank=False, null=False)

# class CardExpansion(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False)
#     expansion = models.ForeignKey(Expansion, on_delete=models.RESTRICT, blank=False, null=False)

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