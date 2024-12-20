# /usr/bin/env python3

import re


def standardize_string(string):
    """
    Original Text       ->      "original_text"
    """
    safe_string = remove_unsafe_chars(string)

    return safe_string.replace(" ", "_").lower()

def remove_unsafe_chars(unsafe_string):
    if not unsafe_string or type(unsafe_string) is not str:
        return ""

    replacement_dict = {
        " ": " ",
        "é": "e",
        "♂": "",
        "♀": "",
    }

    for unsafe_char in replacement_dict:
        unsafe_string = unsafe_string.replace(unsafe_char, replacement_dict[unsafe_char])

    return unsafe_string.strip()


def remove_html_tags(text):
    """
    Original <strong>text</strong>          ->          Original text
    """
    return text if text is None else re.sub(re.compile("<.*?>"), " ", text)