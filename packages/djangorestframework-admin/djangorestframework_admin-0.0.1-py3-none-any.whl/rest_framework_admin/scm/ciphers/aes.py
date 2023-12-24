#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/11
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['AESCipher']

import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from rest_framework_admin.scm.settings import api_settings


class AESCipher:
    """
    加密的一方和解密的一方必须提前确定好key值
    """

    def __init__(self, key=api_settings.AES_KEY, model='ECB',
                 encode_='utf8', iv=None):
        self.encode_ = encode_
        self.model = {'ECB': AES.MODE_ECB, 'CBC': AES.MODE_CBC}[model]
        self.block_size = 16
        self.key = key.encode(self.encode_)
        if model == 'ECB':
            self.aes = AES.new(self.key, self.model)  # 创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key, self.model, iv)  # 创建一个aes对象

    def pad(self, s):
        s = s.encode(self.encode_)
        return pad(s, self.block_size)

    def unpad(self, s):
        return unpad(s, self.block_size)

    def add_16(self, par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def encrypt(self, text):
        text = self.pad(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode()

    def decrypt(self, text):
        text = base64.decodebytes(self.pad(text))
        self.decrypt_text = self.unpad(self.aes.decrypt(text))
        return self.decrypt_text.decode(self.encode_)
