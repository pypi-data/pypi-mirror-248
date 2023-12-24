#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/11
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['Cipher', 'AESCipher']

from scm.ciphers.base import BaseCipher
from scm.ciphers.aes import AESCipher
Cipher = None


def init_cipher():
    global Cipher
    Cipher = BaseCipher()


init_cipher()
