#! /usr/bin/env python3

from cards.models import *

from scripts.db.table_imports.energy_type import import_objects as import_energy_types
from scripts.db.table_imports.set import import_objects as import_sets
from scripts.db.table_imports.attack import import_objects as import_attacks
from scripts.db.table_imports.illustrator import import_objects as import_illustrators
from scripts.db.table_imports.pokemon import import_objects as import_pokemon


print(f"\nStarting import procedure...\n")

# call each import function
import_energy_types()
import_sets()
import_attacks()
import_illustrators()
import_pokemon()

# gather totals for each table
total_energy_types = EnergyType.objects.count()
total_sets = Set.objects.count()
total_attacks = Attack.objects.count()
total_illustrators = Illustrator.objects.count()
total_pokemon = Pokemon.objects.count()

print(f"\nImport scripts have completed. Here are the total records now found in each table:")
print(f"- EnergyType: {total_energy_types}")
print(f"- Set: {total_sets}")
print(f"- Attack: {total_attacks}")
print(f"- Illustrator: {total_illustrators}")
print(f"- Pokemon: {total_pokemon}")

print("\nImport procedure complete.\n")