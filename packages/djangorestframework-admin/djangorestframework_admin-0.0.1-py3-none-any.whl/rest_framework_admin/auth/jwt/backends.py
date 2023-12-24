#!/usr/bin/python
# -*- coding:utf-8 -*-
# DateTime:2023/6/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['AuthBackend']

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings

from auth import logger
from auth.jwt.utils import blacklist


class AuthBackend(ModelBackend):
    def authenticate(self, request, token=None, **kwargs):
        if token is None:
            return None
        request.META[api_settings.AUTH_HEADER_NAME] = f'{api_settings.AUTH_HEADER_TYPES[0]} {token}'
        try:
            user_auth_tuple = JWTAuthentication().authenticate(request)
        except InvalidToken:
            logger.exception(_('IamJwt 无效'))
            user_auth_tuple = None
        except BaseException:
            logger.exception(_('IamJwt 认证失败'))
            user_auth_tuple = None
        finally:
            request.META.pop(api_settings.AUTH_HEADER_NAME)
        if user_auth_tuple is None:
            return None
        user, token = user_auth_tuple
        if blacklist.has_token(token):
            return None
        return user
