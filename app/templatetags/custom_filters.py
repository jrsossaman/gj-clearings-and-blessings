from django import template

register = template.Library()

@register.filter
def chakras_short(value):
    mapping = {
        "open": "O",
        "closed_to_open": "C > O",
        "see_notes": "See Notes"
    }
    return mapping.get(value, value)

@register.filter
def hindrances_short(value):
    mapping = {
        "dark_entities": "DA's",
        "attacks": "Attacks",
        "societal": "Societal",
        "viruses": "Viruses"
    }
    return mapping.get(value, value)