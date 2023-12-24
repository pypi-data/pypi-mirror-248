#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = [
    'PermissionFilter',
]

from django_filters import rest_framework as filters

from permission.models import Permission


class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    role_id = filters.CharFilter(field_name='roles__id')

    class Meta:
        model = Permission
        fields = ['name', 'role_id']
