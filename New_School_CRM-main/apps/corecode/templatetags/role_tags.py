from django import template
register = template.Library()

@register.filter
def is_role(user, role_name):
    try:
        return user.userprofile.role == role_name
    except:
        return False
