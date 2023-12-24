#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from enum import Enum

from django.conf import settings


class TokenEnum(Enum):
    access = 'access'
    refresh = 'refresh'


class CookieEnum(Enum):
    access = f'{settings.APP_CODE}_{TokenEnum.access.value}'
    refresh = f'{settings.APP_CODE}_{TokenEnum.refresh.value}'
