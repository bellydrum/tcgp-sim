from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# string replacement

@register.filter()
@stringfilter
def to_under(value, arg):
    """
    arg=" "         "this text"     ->      "this_text"
    arg="-"         "this-text"     ->      "this_text"
    """
    return value.replace(arg, "_")

@register.filter()
@stringfilter
def to_hyphen(value, arg):
    """
    arg=" "         "this text"     ->      "this-text"
    arg="-"         "this_text"     ->      "this-text"
    """
    return value.replace(arg, "-")

@register.filter(is_safe=True)
@stringfilter
def no_unsafe(value):
    """
    "Pokémon"       ->          "Pokemon"
    "Flabébé        ->          "Flabebe"
    """
    unsafe_dict = {
        "é": "e",
        "♂": "",
        "♀": "",
        ".": "",
        "'": ""
    }

    for unsafe_char in unsafe_dict:
        value = value.replace(unsafe_char, unsafe_dict[unsafe_char])
    
    return value