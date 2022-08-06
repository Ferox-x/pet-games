from django import template

register = template.Library()


def convert_time(time):
    format_time = '0' + str(time) if time < 10 else str(time)
    return format_time


@register.simple_tag
def format_schulte(record, game):
    if game == 'schulte':
        minute_raw = record // (60 * 100)
        record = record % (60 * 100)

        second_raw = record // 100
        record = record % 100

        mil_sec_raw = record

        minute = convert_time(minute_raw)
        second = convert_time(second_raw)
        mil_sec = convert_time(mil_sec_raw)

        return '{minute}:{second}:{mil_sec}'.format(minute=minute,
                                                    second=second,
                                                    mil_sec=mil_sec)
    return record


@register.simple_tag
def rating_position(index, page):
    position = index + (25 * (page - 1))
    return position

