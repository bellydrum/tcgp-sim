# /usr/bin/env python3

import re


def standardize_string(string, no_spaces=False, lower=False):
    """
    Original Text       ->      "original_text"
    """
    # Step 1. Remove all unsafe characters
    string = remove_unsafe_chars(string)

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
    return text if text is None else re.sub(re.compile("<.*?>"), " ", text)