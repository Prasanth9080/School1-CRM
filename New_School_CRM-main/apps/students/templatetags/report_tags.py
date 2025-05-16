# apps/students/templatetags/report_tags.py

from django import template

register = template.Library()

@register.filter(name='value_or_dash')
def value_or_dash(value):
    return value if value not in [None, ""] else "-"
