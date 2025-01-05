from django.db import models


class CardTypes(models.TextChoices):
    POKEMON = "P"
    TRAINER = "T"

class EnergyTypes(models.TextChoices):
    COLORLESS = "C"
    DARKNESS = "D"
    FIGHTING = "Fg"
    FIRE = "Fi"
    GRASS = "G"
    LIGHTNING = "L"
    METAL = "M"
    PSYCHIC = "P"
    WATER = "W"

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



    {
        "name": "Colorless",
        "name_display": "Colorless"
    },
    {
        "name": "Darkness",
        "name_display": "Darkness"
    },
    {
        "name": "Fighting",
        "name_display": "Fighting"
    },
    {
        "name": "Fire",
        "name_display": "Fire"
    },
    {
        "name": "Grass",
        "name_display": "Grass"
    },
    {
        "name": "Lightning",
        "name_display": "Lightning"
    },
    {
        "name": "Metal",
        "name_display": "Metal"
    },
    {
        "name": "Psychic",
        "name_display": "Psychic"
    },
    {
        "name": "Water",
        "name_display": "Water"
    }