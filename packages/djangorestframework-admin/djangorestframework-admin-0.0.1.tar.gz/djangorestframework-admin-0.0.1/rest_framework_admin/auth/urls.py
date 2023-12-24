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

from rest_framework_admin.decorators import login_exempt
from auth import views

urlpatterns = [
    path(r'jwt/', include('auth.jwt.urls')),
    re_path(r'me/$', views.AuthMeRetrieveAPIView.as_view()),
    re_path(
        r'register/$',
        login_exempt(
            views.AuthRegisterCreateAPIView.as_view())),
]
