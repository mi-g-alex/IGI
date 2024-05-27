import calendar

from django import template

register = template.Library()


@register.filter
def first_sentence(text):
    sentences = text.split('.')
    if sentences:
        return sentences[0] + '.' if sentences[0] else ''
    return ''
