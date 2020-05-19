from django import template
from django.contrib.auth.models import Group
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    try:
        if group in user.groups.all():
            print('True')
            return True
    except:
        # print('False')
        # if group =="customer":
        #     return True
        return False
    #
    # print(user.groups.all())
    # return True if group in user.groups.all() else False

@register.simple_tag
def update_variable(value):
    print('update_varialbvle',value)
    data = value
    return data