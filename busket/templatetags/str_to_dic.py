from django import template
import json

register = template.Library()

@register.filter
def str_to_dict(value):
	return json.loads(value)
