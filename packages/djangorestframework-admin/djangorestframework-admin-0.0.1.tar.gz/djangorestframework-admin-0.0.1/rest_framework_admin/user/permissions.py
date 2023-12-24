#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/12/8
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = [
    'UserModelPermission',
    'GroupModelPermission',
    'UserRelatedGroupModelPermission',
    'GroupRelatedUserModelPermission']

from rest_framework import permissions


class UserModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('selection', 'update_password'):
            return True
        return request.user.is_administrator()

    def has_object_permission(self, request, view, obj):
        return request.user.is_administrator()


class GroupModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('selection', ):
            return True
        return request.user.is_administrator()

    def has_object_permission(self, request, view, obj):
        if request.user.is_administrator():
            return True
        return obj.create_user_id == request.user.id


class UserRelatedGroupModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_administrator():
            return True
        # 仅允许操作用户自己的
        user = view.get_parent_object()
        return request.user.id == user.id

    def has_object_permission(self, request, view, obj):
        if request.user.is_administrator():
            return True
        # 仅允许操作用户自己的
        user = view.get_parent_object()
        return request.user.id == user.id


class GroupRelatedUserModelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_administrator():
            return True
        # 仅允许操作用户自己创建的
        group = view.get_parent_object()
        return request.user.id == group.create_user_id

    def has_object_permission(self, request, view, obj):
        if request.user.is_administrator():
            return True
        # 仅允许操作用户自己创建的
        group = view.get_parent_object()
        return request.user.id == group.create_user_id
