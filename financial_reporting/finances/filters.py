from django import template


register = template.Library()

@register.filter
def group_filter(user, group_name):
    return user.groups.filter(name=group_name).exists()