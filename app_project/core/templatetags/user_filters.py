from django import template

register = template.Library()


@register.filter
def addclass(field, css: str) -> str:
    """Тег добавляющий классы в форму."""
    return field.as_widget(attrs={'class': css})
