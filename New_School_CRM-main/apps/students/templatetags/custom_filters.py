# from django import template

# register = template.Library()

# @register.filter
# def getattr(obj, attr):
#     return getattr(obj, attr, None)





from django import template

register = template.Library()

# @register.filter
# def getattr(obj, attr_name):
#     return getattr(obj, attr_name, '-')
@register.filter
def getattr(obj, attr_with_default):
    # Handles format like "subject,default"
    if ',' in attr_with_default:
        attr, default = attr_with_default.split(',', 1)
    else:
        attr, default = attr_with_default, ''
    return getattr(obj, attr, default)
