#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/2/27
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['AuthModelMiddleware']

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

from auth.jwt.exceptions import AuthVerifyError
from rest_framework_admin.decorators import is_login_exempt


class AuthMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        if any([is_login_exempt(request, view),
                request.is_login_exempt(),
                request.user.is_authenticated]):
            return None
        user = auth.authenticate(request=request)
        if user and user.is_authenticated:
            # 登录成功，确认登陆正常后退出
            request.user = user
            return None
        return AuthVerifyError().to_response()
