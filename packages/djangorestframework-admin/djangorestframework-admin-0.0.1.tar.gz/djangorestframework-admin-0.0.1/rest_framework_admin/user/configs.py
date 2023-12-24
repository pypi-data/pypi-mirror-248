#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""

from enum import Enum


class DefaultUserEnum(Enum):
    # username=id
    root = '0' * 32
    admin = '0' * 30 + '10'
    test = '0' * 29 + '100'



