from django.contrib.auth.models import Group, Permission


def create_group_user(*args, **kwargs):  # noqa
    group, is_created = Group.objects.get_or_create(name='Customer')
    if not is_created:
        return
    shop_perms = list(Permission.objects.filter(content_type__app_label='shop', name__contains='view').values('pk'))
    user_perms = list(Permission.objects.filter(content_type__app_label__in=['users', 'profiles']).values('pk'))
    cart_perms = list(Permission.objects.filter(content_type__app_label='cart').values('pk'))
    perms = shop_perms + cart_perms + user_perms
    group.permissions.set([perm['pk'] for perm in perms])
