#!/usr/bin/python
# -*- coding:utf-8 -*-
# DateTime:2023/6/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['AuthMiddleware']

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.settings import api_settings

from auth.jwt.exceptions import AuthVerifyError
from rest_framework_admin.decorators import is_login_exempt
from auth.jwt.configs import CookieEnum


class AuthMiddleware(MiddlewareMixin):

    def process_view(self, request, view, args, kwargs):
        if any([is_login_exempt(request, view),
                request.is_login_exempt(),
                request.user.is_authenticated]):
            return None
        token = request.META.get(
            api_settings.AUTH_HEADER_NAME,
            request.COOKIES.get(
                CookieEnum.access.name,
                None))
        if not token:
            return None
        user = auth.authenticate(request=request, token=token)
        # from user.models import User
        # user = User.objects.get(id='f571c302f55a31b1a7f6147ac8f5480e')
        if user and user.username != request.user.username:
            request.user = user
        if request.user.is_authenticated:
            return None
        return AuthVerifyError().to_response()
