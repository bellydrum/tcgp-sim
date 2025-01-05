import json
from django.db import models

from cards.enums import *


# abstract and parent models

class Rarity(models.Model):
    id = models.BigAutoField(primary_key=True)
    rarity_id = models.CharField(max_length=8, blank=False, null=False, choices=Rarities.choices)
    name = models.CharField(max_length=64, blank=False, null=False)
    name_display = models.CharField(max_length=64, blank=False, null=False)

class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    pokedex_number = models.SmallIntegerField(blank=False, null=True)                                           # 91
    name = models.CharField(max_length=128)                                                                     # "cloyster"
    name_display = models.CharField(max_length=128, blank=False)                                                # "Cloyster"
    active = models.BooleanField(blank=False, null=False, default=True)                                         # True
    ability_ids = models.JSONField(blank=False, null=True, verbose_name="card_ability_ids")
    attack_ids = models.JSONField(blank=False, null=True, verbose_name="card_attack_ids")                       # ["PK_01_00010_01"]
    card_id = models.CharField(max_length=64, blank=False, null=True)                                           # "PK_10_000670_00"
    card_pokemon_id = models.CharField(max_length=64, blank=False, null=True)                                   # "PK_10_000670_00"
    card_trainer_id = models.CharField(max_length=64, blank=False, null=True)                                   # "PK_10_000670_00"
    card_trainer_type = models.CharField(max_length=1, null=True, choices=TrainerTypes.choices)                 # None | ("S", "I")
    card_type = models.CharField(max_length=128, choices=CardTypes.choices)                                     # "pokemon"
    character_id = models.CharField(max_length=128, blank=False, null=True)                                     # "PARSHEN"
    collection_number = models.SmallIntegerField(blank=False, null=True)                                        # 67
    description = models.CharField(max_length=2048, blank=False, null=True)                                     # ""
    dust_cost = models.IntegerField(blank=False, null=True)                                                     # 70
    effect = models.JSONField(blank=False, null=True, verbose_name="card_effect")                               # "{...}"
    expansion_id = models.CharField(max_length=64, blank=False, null=True)                                      # "A1"
    flavor_text = models.CharField(max_length=2048, blank=False, null=True)                                     # "Cloyster that live in seas..."
    image_url = models.CharField(max_length=5096, blank=False, null=True)
    is_promo = models.BooleanField(blank=False, null=True)                                                      # False
    is_serial = models.BooleanField(blank=False, null=True)                                                     # False
    promotion_name = models.CharField(max_length=512, blank=False, null=True)                                   # None
    rarity = models.ForeignKey(Rarity, on_delete=models.RESTRICT, blank=False, null=True)                       # <Rarity object>
    rules_description = models.CharField(max_length=2048, blank=False, null=True)                               # "..."
    series_id = models.CharField(max_length=8, blank=False, null=True)                                          # "A"
    variants = models.JSONField(blank=False, null=True, verbose_name="card_variants")                           # "['PK_10_000670_00', 'PK_10_000671_00']"

""" import destinations """

class Ability(models.Model):
    id = models.BigAutoField(primary_key=True)
    ability_id = models.CharField(max_length=512, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)                                            # "gas_leak"
    name_display = models.CharField(max_length=200, blank=False, null=True)                                     # "Gas Leak"
    description = models.CharField(max_length=512, blank=False, null=True)
    effect = models.CharField(max_length=512, blank=False, null=True)

class Attack(models.Model):
    id = models.BigAutoField(primary_key=True)
    attack_id = models.CharField(max_length=512, blank=False, null=False)                                       # "PK_002780_ATK_01"
    name = models.CharField(max_length=200, blank=False, null=False)                                            # "surprise_attack"
    name_display = models.CharField(max_length=200, blank=False, null=True)                                     # "Surprise Attack"
    cost = models.JSONField(blank=False, null=True, verbose_name="attack_cost")                                 # '{"psychic": 1}'
    damage = models.IntegerField(blank=False, null=True)                                                        # 50 | None
    is_no_damage = models.BooleanField(null=True)                                                               # False
    damage_symbol = models.CharField(max_length=8, blank=False, null=True)                                      # "+"
    effect = models.JSONField(blank=False, null=True, verbose_name="attack_effect")                             # <function_name>
    description = models.CharField(max_length=512, blank=False, null=True)                                      # "Flip a coin. If tails, this attack does nothing."

    def get_cost_icons_html(self):
        cost_object = json.loads(self.cost)

        cost_icon_links = []

        for energy_type, amount in cost_object.items():
            for i in range(amount):
                cost_icon_links.append(energy_type.lower())

        return cost_icon_links

class EnergyType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    name_display = models.CharField(max_length=64, blank=False, null=True)

class Expansion(models.Model):
    id = models.BigAutoField(primary_key=True)
    expansion_id = models.CharField(max_length=64, blank=False, null=True)                                      # "A1", "A1a"
    name = models.CharField(max_length=512, blank=False, null=True)                                             # "genetic_apex"
    name_display = models.CharField(max_length=512, blank=False, null=True)                                     # "Genetic Apex"
    card_count = models.IntegerField(blank=False, null=True)                                                    # 226
    is_promo = models.BooleanField()                                                                            # False
    sort_number = models.IntegerField(blank=False, null=True)                                                   # 1

class Illustrator(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=False, null=False)

class Pack(models.Model):
    id = models.BigAutoField(primary_key=True)
    pack_id = models.CharField(max_length=64, blank=False, null=True)                                           # "A1", "A1a"
    name = models.CharField(max_length=512, blank=False, null=True)                                             # "mewtwo_pack"
    name_display = models.CharField(max_length=512, blank=False, null=True)                                     # "Mewtwo Pack"
    expansion = models.ForeignKey(Expansion, on_delete=models.RESTRICT, blank=False, null=True)                 # <Expansion object>
    sort_number = models.SmallIntegerField(blank=False, null=True)                                              # 30

class Pokemon(Card, models.Model):
    pokemon_id = models.CharField(max_length=512, blank=False, null=False)                                      # "PK_000340"
    stage_number = models.SmallIntegerField(blank=False, null=True)                                             # 1
    stage_name = models.CharField(max_length=16, null=True, choices=Stages.choices)                             # "Stage 1"
    hp = models.SmallIntegerField(blank=False, null=True)                                                       # 90
    is_ex = models.BooleanField(blank=False, null=True)                                                         # False
    ability = models.CharField(max_length=64, blank=False, null=True)
    ability_description = models.CharField(max_length=1024, blank=False, null=True)
    previous_evolution = models.CharField(max_length=512, blank=False, null=True)                               # "PK_000339"
    retreat_cost_number = models.SmallIntegerField(blank=False, null=True)                                      # 2
    retreat_cost_type = models.ForeignKey(EnergyType, on_delete=models.RESTRICT, blank=False, null=True, related_name="pokemon_retreat_cost_type")
    weakness_type = models.ForeignKey(EnergyType, on_delete=models.RESTRICT, blank=False, null=True, related_name="pokemon_weakness_type")

class Trainer(Card, models.Model):
    trainer_id = models.CharField(max_length=512, blank=False, null=False)                                      # "TR_000230"
    trainer_type = models.CharField(max_length=1, null=True, choices=TrainerTypes.choices)                      # ("S", "I")
    trainer_type_label = models.CharField(max_length=32, blank=False, null=True)                                # "Supporter"

##################################
# relational models (many-to-many)
##################################

class CardAbility(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "ability"], name="unique_card_ability")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    ability = models.ForeignKey(Ability, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")

class CardAttack(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "attack"], name="unique_card_attack")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    attack = models.ForeignKey(Attack, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")

class CardIllustrator(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["card", "illustrator"], name="unique_card_illustrator")
        ]
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    illustrator = models.ForeignKey(Illustrator, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")

class CardPack(models.Model):
    id = models.BigAutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    pack = models.ForeignKey(Pack, on_delete=models.RESTRICT, blank=False, null=False, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")