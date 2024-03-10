from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='censor')
@stringfilter
def censor(value):
    bad_words = ['Trump', 'Biden', 'Vivek', 'Musk', 'Harris', ]
    for word in bad_words:
        value = value.replace(word, word[0] + '*' * (len(word) - 1))
    return value
