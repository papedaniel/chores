from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='overdue')
def overdue(value, frequency):
    dt = timezone.now() - value
    days = dt.days - frequency
    return days
