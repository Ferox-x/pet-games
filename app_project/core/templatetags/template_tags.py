from django import template

register = template.Library()


@register.simple_tag
def header_max_len(header: str):
    return header[:20] + '...'


@register.simple_tag
def message_max_len(message: str):
    return message[:60] + '...'
