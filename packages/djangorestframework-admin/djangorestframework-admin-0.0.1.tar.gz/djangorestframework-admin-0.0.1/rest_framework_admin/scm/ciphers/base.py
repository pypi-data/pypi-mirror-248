#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/11
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['BaseCipher']

import shutil


class BaseCipher:
    def __init__(self):
        self.init_cipher()

    def init_cipher(self):
        self.cipher = None

    def encrypt(self, file_path, *args, **kwargs):
        return True

    def decrypt(self, encrypted_file_path, decrypted_file_path):
        with open(encrypted_file_path, 'rb') as enc_fd, open(decrypted_file_path, 'ab+') as dec_fd:
            shutil.copyfileobj(enc_fd, dec_fd)
        return True

    def is_encrypted(self, file_path):
        return True
