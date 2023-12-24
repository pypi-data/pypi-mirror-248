#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/12/22
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = [
    'RoleModelPermission',
    'RoleRelatedPermissionModelPermission',
    'RoleRelatedSubjectModelPermission',
    'SubjectListPermission']

from rest_framework import permissions


class RoleModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('selection', ):
            return True
        return request.user.is_administrator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_administrator()


class RoleRelatedPermissionModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_administrator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_administrator()


class RoleRelatedSubjectModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_administrator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_administrator()


class SubjectListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_administrator()
