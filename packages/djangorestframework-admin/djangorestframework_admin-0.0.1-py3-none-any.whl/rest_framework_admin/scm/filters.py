#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/10
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['ConfigFilter']

from django_filters import rest_framework as filters

from scm.models import Config


class ConfigFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = Config
        fields = ['name']

    def filter_by_name(self, queryset, name, value):
        names = value.split(',')
        return queryset.filter(name__in=names)
