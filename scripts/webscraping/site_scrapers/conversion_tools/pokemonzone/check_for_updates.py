def get_removed_and_new_card_ids(existing_cards, formatted_cards) -> tuple:
    """
    @input
        existing_cards                  dict                    Card objects read from a JSON file in data/imports/
        formatted_cards                 dict                    Card objects from an API response

    @returns                            tuple(list, list)       A list of removed card_ids and a list of new card_ids.
                                                                Both lists may be empty.
    """
    existing_object_card_ids = [existing_card["card_id"] for existing_card in existing_cards]
    incoming_object_card_ids = [incoming_card["card_id"] for incoming_card in formatted_cards]

    def get_left_exclusive(set_1, set_2):
        return [object_card_id for object_card_id in filter(lambda card_id: card_id not in set_2, set_1)]

    return get_left_exclusive(existing_object_card_ids, incoming_object_card_ids), get_left_exclusive(incoming_object_card_ids, existing_object_card_ids)