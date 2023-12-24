#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/16
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['api_settings']

from django.conf import settings

from rest_framework_admin.settings import get_api_settings

DEFAULTS = {
    'MINIO_BUCKET': settings.MINIO_BUCKET,
    'USER_ICON_MINIO_PREFIX': 'user/icons',
}

api_settings = get_api_settings('USER', defaults=DEFAULTS)


