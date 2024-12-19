import json
from django.db.utils import IntegrityError

from cards.models import *
from scripts.db.table_imports.pokemon import import_objects as import_pokemon
from scripts.db.table_imports.supporter import import_objects as import_supporters
from scripts.db.table_imports.item import import_objects as import_items


def import_objects():
    Card.objects.all().delete()

    import_pokemon()
    import_supporters()
    import_items()