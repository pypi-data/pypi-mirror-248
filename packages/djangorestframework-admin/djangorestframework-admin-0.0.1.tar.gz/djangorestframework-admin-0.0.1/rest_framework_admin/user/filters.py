#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = [
    'UserFilter',
    'GroupFilter',
    'UserRelatedGroupFilter',
    'GroupRelatedUserFilter'
]

from django_filters import rest_framework as filters

from rest_framework_admin.user.models import User, Group, UserGroupRel


class UserFilter(filters.FilterSet):
    role_id = filters.CharFilter(method='filter_by_role_id')
    group_id = filters.CharFilter(field_name='groups__id')
    is_active = filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['role_id', 'is_active', 'group_id']

    def filter_by_role_id(self, queryset, name, value):
        from role.models import Role
        role = Role.objects.filter(pk=value).first()
        if not role:
            return User.objects.none()
        return role.filter_users(is_valid=True) & queryset


class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    role_id = filters.CharFilter(method='filter_by_role_id')

    class Meta:
        model = Group
        fields = ['name', 'role_id']

    def filter_by_role_id(self, queryset, name, value):
        from role.models import Role
        role = Role.objects.filter(pk=value).first()
        if not role:
            return Group.objects.none()
        return role.filter_groups(is_valid=True) & queryset


class UserRelatedGroupFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='group_id')

    name = filters.CharFilter(
        lookup_expr='icontains',
        field_name='group__name')

    class Meta:
        model = UserGroupRel
        fields = ['id', 'name']


class GroupRelatedUserFilter(filters.FilterSet):
    id = filters.CharFilter(field_name='user_id')

    name = filters.CharFilter(
        lookup_expr='icontains',
        field_name='user__username')

    class Meta:
        model = UserGroupRel
        fields = ['id', 'name']
