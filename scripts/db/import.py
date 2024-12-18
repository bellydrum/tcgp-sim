#! /usr/bin/env python3

from cards.models import *

from scripts.db.table_imports.energy_type import import_objects as import_energy_types
from scripts.db.table_imports.rarity import import_objects as import_rarities
from scripts.db.table_imports.attack import import_objects as import_attacks
from scripts.db.table_imports.card import import_objects as import_cards
from scripts.db.table_imports.card_illustrator import import_objects as import_card_illustrators
from scripts.db.table_imports.expansion import import_objects as import_expansions
from scripts.db.table_imports.illustrator import import_objects as import_illustrators
from scripts.db.table_imports.card_pack import import_objects as import_card_packs
from scripts.db.table_imports.pack import import_objects as import_packs
from scripts.db.table_imports.card_attack import import_objects as import_card_attacks


print(f"\nStarting import procedure...\n")

# call each import function
import_rarities()
import_energy_types()
import_expansions()
import_packs()
import_attacks()
import_illustrators()
import_cards()
import_card_attacks()
import_card_illustrators()
import_card_packs()

# gather totals for each table
total_rarities = Rarity.objects.count()
total_cards = Card.objects.count()
total_attacks = Attack.objects.count()
total_energy_types = EnergyType.objects.count()
total_expansions = Expansion.objects.count()
total_illustrators = Illustrator.objects.count()
total_packs = Pack.objects.count()
total_pokemon = Pokemon.objects.count()
total_trainers = Trainer.objects.count()
total_card_attacks = CardAttack.objects.count()
total_card_illustrators = CardIllustrator.objects.count()
total_card_packs = CardPack.objects.count()

print(f"\nImport scripts have completed. Here are the total records now found in each table:")
print(f"- Rarities: {total_rarities}")
print(f"- Cards: {total_cards}")
print(f"- Attacks: {total_attacks}")
print(f"- EnergyTypes: {total_energy_types}")
print(f"- Expansions: {total_expansions}")
print(f"- Illustrators: {total_illustrators}")
print(f"- Packs: {total_packs}")
print(f"- Pokemon: {total_pokemon}")
print(f"- Trainers: {total_trainers}")
print(f"- CardAttacks: {total_card_attacks}")
print(f"- CardIllustrators: {total_card_illustrators}")
print(f"- CardPacks: {total_card_packs}")

print("\nImport procedure complete.\n")