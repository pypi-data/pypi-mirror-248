#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['urlpatterns']

from django.urls import path, include, re_path
from rest_framework import routers

from permission import views

permission_router = routers.DefaultRouter()
permission_router.register(r'^permissions', views.PermissionViewSet)

urlpatterns = [
    path(r'', include(permission_router.urls)),
]
