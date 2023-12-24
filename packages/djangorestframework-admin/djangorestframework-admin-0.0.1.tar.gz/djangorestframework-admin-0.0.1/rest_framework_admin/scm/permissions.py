#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/19
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['ConfigPermission']

from rest_framework import permissions


class ConfigPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method.lower() in ('get', ):
            return True
        if not (request.user and request.user.is_authenticated):
            return False
        return is_iam_admin(request)

    def has_object_permission(self, request, view, obj):
        if request.method.lower() in ('get', ):
            return True
        if not (request.user and request.user.is_authenticated):
            return False
        return is_iam_admin(request)
