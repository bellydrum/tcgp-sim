# /usr/bin/env python3

import re

from cards.models import EnergyType


# TODO -- move this shit.
energy_type_text = [
    "colorless",
    "darkness",
    "fighting",
    "fire",
    "grass",
    "lightning",
    "metal",
    "psychic",
    "water"
]

def standardize_string(string, no_spaces=False, lower=False):
    """
    Original Text       ->      "original_text"
    """
    # Step 1. Remove all unsafe characters
    string = remove_unsafe_chars(string)

    string = replace_icon_html_with_icon_name(string)

    # Step 2. Remove HTML tags
    string = remove_html_characters(string)

    # Step 3. Remove consecutive whitespace characters
    string = re.sub("\s{2,}", " ", string)

    # Step 4. Remove consecutive whitespace characters
    string = re.sub("\s{2,}", " ", string)

    # Step 4 (OPTIONAL). Replace spaces with underscores
    if no_spaces == True:
        string = string.replace(" ", "_")

    # Step 5 (OPTIONAL). Lowercase the string
    if lower == True:
        string = string.lower()

    return string

def replace_icon_html_with_icon_name(string):
    """
    Looks for a specific instance of an HTML reference to an Energy icon and replaces it with the icon name.
    """
    if """<span class="energy-text energy-text--type-""" in string:
        for energy_type in energy_type_text:
            if f"""<span class="energy-text energy-text--type-{energy_type}""" in string:
                string = re.sub(
                    f"""<span class="energy-text energy-text--type-{energy_type}"></span>""",
                    energy_type.title(),
                    string
                )

    return string

def remove_unsafe_chars(unsafe_string):
    if not unsafe_string or type(unsafe_string) is not str:
        return ""

    replacement_dict = {
        " ": " ",
        "é": "e",
        "♂": "",
        "♀": "",
        "’": "'",
        "\u002B": "+",
        "\u2212": "-",
    }

    for unsafe_char in replacement_dict:
        unsafe_string = unsafe_string.replace(unsafe_char, replacement_dict[unsafe_char])

    return unsafe_string.strip()


def remove_html_characters(text):
    """
    Original <strong>text</strong>          ->          Original text
    """
    fixed_text = text if text is None else re.sub(re.compile("<.*?>"), " ", text)

    text = re.sub(" \,", ",", fixed_text)
    text = re.sub(" \.", "", text)
    text = re.sub(" \:", "", text)
    
    return text