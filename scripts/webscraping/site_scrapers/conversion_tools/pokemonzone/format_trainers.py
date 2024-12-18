import json
from pprint import pprint


def format_trainer_object(trainer_object):
    return {
        "trainer_id": trainer_object.get("trainerId"),
        "trainer_type": trainer_object.get("trainerTypeLabel"),
    }

def extract_trainers_from_card_objects(formatted_trainer_cards):
    return formatted_trainer_cards, [card.get("trainer_object") for card in formatted_trainer_cards]