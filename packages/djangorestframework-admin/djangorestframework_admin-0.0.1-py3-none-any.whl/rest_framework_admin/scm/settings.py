#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/10
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['api_settings']

from django.conf import settings

from rest_framework_admin.settings import APISettings

DEFAULTS = {
    'AES_KEY': 'KeyWord',
    'MINIO_BUCKET': settings.MINIO_BUCKET,
    # 图像类型文件支持的扩展名
    'IMAGE_EXTS': ('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.webp', '.svg', '.icon', '.tif'),
    # 文件类型文件支持加解密的扩展名
    'CIPHER_FILE_EXTS': ('.parquet', '.csv', '.tsv', '.xls', '.xlsx'),
    # 临时上传目录
    'TMP_UPLOAD_DIR': '/tmp/'
}

api_settings = APISettings('SCM', None, DEFAULTS)
