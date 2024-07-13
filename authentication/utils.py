from django.contrib.auth.models import Group

def is_member(user, group_name):
    return Group.objects.filter(name=group_name, user=user).exists()
