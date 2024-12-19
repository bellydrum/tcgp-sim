from django.db import models


class CardTypes(models.TextChoices):
    POKEMON = "P"
    TRAINER = "T"

class TrainerTypes(models.TextChoices):
    ITEM = "I"
    SUPPORTER = "S"

class Rarities(models.TextChoices):
    COMMON = "C"
    UNCOMMON = "U"
    RARE = "R"
    DOUBLE_RARE = "RR"
    ART_RARE = "AR"
    SUPER_RARE = "SR"
    IMMERSIVE = "IM"
    CROWN_RARE = "UR"
    SPECIAL_ART_RARE = "SAR"