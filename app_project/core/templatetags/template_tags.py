from django import template

register = template.Library()


@register.simple_tag
def header_max_len(header: str):
    if len(header) > 20:
        return header[:20] + '...'
    return header


@register.simple_tag
def message_max_len(message: str):
    if len(message) > 60:
        return message[:60] + '...'
    return message
