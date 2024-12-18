#! /usr/bin/env python3

from cards.models import *

from scripts.db.import_scripts.card_category import import_objects as import_card_category
from scripts.db.import_scripts.energy_type import import_objects as import_energy_types
from scripts.db.import_scripts.rarity import import_objects as import_rarities
from scripts.db.import_scripts.sets import import_objects as import_sets
from scripts.db.import_scripts.attack import import_objects as import_attacks
from scripts.db.import_scripts.pokemon import import_objects as import_pokemon


print(f"\nStarting import procedure...")

# call each import function
import_card_category()
import_energy_types()
import_rarities()
import_sets()
import_attacks()
import_pokemon()

# gather totals for each table
total_card_categories = CardCategory.objects.count()
total_energy_types = EnergyType.objects.count()
total_rarities = Rarity.objects.count()
total_sets = Set.objects.count()
total_attacks = Attack.objects.count()
total_pokemon = Pokemon.objects.count()

print(f"\nImport complete. Here are the total records now found in each table:")
print(f"- CardCategory: {total_card_categories}")
print(f"- EnergyType: {total_energy_types}")
print(f"- Rarity: {total_rarities}")
print(f"- Set: {total_sets}")
print(f"- Attack: {total_attacks}")
print(f"- Pokemon: {total_pokemon}")