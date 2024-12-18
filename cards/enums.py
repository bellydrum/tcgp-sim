from django.db import models


class CardTypes(models.TextChoices):
    POKEMON = "P"
    TRAINER = "T"

class TrainerTypes(models.TextChoices):
    FOSSIL = "F"
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
    ULTRA_RARE = "UR"
    SPECIAL_ART_RARE = "SAR"

class Stages(models.TextChoices):
    BASIC = "Basic"
    STAGE_1 = "Stage 1"
    STAGE_2 = "Stage 2"