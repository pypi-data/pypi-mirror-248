#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/10/10
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = [
    'post_upload_request',
    'post_upload_success_request',
    'FileInfo',
    'UploadBaseView',
    'UploadView',
    'UploadSuccessView']
import os
import shutil
import tempfile
from io import BytesIO

import cv2
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework_admin.core.storage import storage
from scm.ciphers import Cipher
from scm.configs import FileTypeEnum
from utils.unique import uuid_id

from typing import NamedTuple


class FileInfo(NamedTuple):
    # 最终的存储路径为{dir_path}/{随机id}.{文件格式}
    # 文件类型
    file_type: str
    # 当分片时，用于创建临时文件夹
    file_id: str
    # 文件目录（自定义）,上传到minio时的prefix
    dir_path: str
    # 任务id
    task_id: str
    # 分片序号，-1表示不分片
    chunk: int
    # 分片上传成功后使用
    file_name: str


def __tmp_dir():
    return tempfile.TemporaryDirectory(prefix=f'{settings.APP_CODE}__', dir='/tmp')


def __upload(request, file_info, file_obj, app_settings):
    file_name = uuid_id() + '.' + file_obj.name.rsplit(".")[-1]
    prefix = file_info.dir_path
    if file_info.file_type == FileTypeEnum.video.name:
        dst_path = f'/{app_settings.MINIO_BUCKET}/{prefix}/{file_name}'
        storage.upload_file(file_obj, dst_path)
        url = storage.to_http(dst_path, request=request)
        # 获取关键帧作为封面
        with __tmp_dir() as tmp_dir:
            file_path = os.path.join(tmp_dir, file_name)
            file_obj.seek(0, 0)
            with open(file_path, 'wb') as fd:
                fd.write(file_obj.read())
            cap = cv2.VideoCapture(file_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, 10)  # keys_frame为关键帧的序号
            flag, frame = cap.read()  # frame为关键帧图片，Mat类型
            poster = ""
            if flag:
                img = cv2.resize(frame, None, fx=0.5, fy=0.5)
                # 保存图片质量改为75
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
                result, encimg = cv2.imencode('.jpg', img, encode_param)
                img = BytesIO(encimg)
                file_name = file_info.task_id + ".jpg"  # 文件保存名称
                dst_path = f'/{app_settings.MINIO_BUCKET}/{file_info.task_id}/{file_name}'
                storage.upload_file(img, dst_path)
                url = storage.to_http(dst_path, request=request)
            cap.release()
        return {"path": url, "poster": poster}
    elif file_info.file_type == FileTypeEnum.file.name:
        _, file_ext = os.path.splitext(file_obj.name)
        if file_ext in app_settings.CIPHER_FILE_EXTS:
            # 解密文件
            with __tmp_dir() as tmp_dir:
                file_path = os.path.join(tmp_dir, file_name)
                encrypted_file_path = file_path + '.encrypted'
                decrypted_file_path = file_path + '.decrypted'
                # 将上传的文件保存到本地
                with open(encrypted_file_path, "wb+") as encrypted_fd:
                    encrypted_fd.write(file_obj.read())
                if Cipher.is_encrypted(encrypted_file_path) == 0:
                    # 解密
                    return_code = Cipher.decrypt(
                        encrypted_file_path, decrypted_file_path)
                    if return_code != 0:
                        raise ValidationError(f'文件解密失败，code={return_code}.')
                else:
                    decrypted_file_path = encrypted_file_path
                with open(decrypted_file_path, 'rb') as fd:
                    dst_path = f'/{app_settings.MINIO_BUCKET}/{prefix}/{file_name}'
                    storage.upload_file(fd, dst_path)
                    url = storage.to_http(dst_path, request=request)
        else:
            dst_path = f'/{app_settings.MINIO_BUCKET}/{prefix}/{file_name}'
            storage.upload_file(file_obj, dst_path)
            url = storage.to_http(dst_path, request=request)
    elif file_info.file_type == FileTypeEnum.image.name:
        _, file_ext = os.path.splitext(file_obj.name)
        if file_ext in app_settings.IMAGE_EXTS:
            dst_path = f'/{app_settings.MINIO_BUCKET}/{prefix}/{file_name}'
            storage.upload_file(file_obj, dst_path)
            url = storage.to_http(dst_path, request=request)
        else:
            raise ValidationError(f'图像格式错误[{file_ext}]')
    else:
        raise ValidationError(f'不支持的文件类型[{file_info.file_type}]')
    return {"path": url}


def post_upload_request(request, file_info, file_obj, app_settings):
    """ 上传文件的请求

    :param Request request: Request
    :param FileInfo file_info: 文件信息
    :param IO file_obj: 文件对象
    :param app_settings: 应用的settings
    :return: Response
    :rtype: Response
    """
    if not file_obj:
        raise ValidationError(_('文件无效'))
    if file_info.chunk == -1:
        # 不分片，直接上传
        data = __upload(request, file_info, file_obj, app_settings)
        return Response(data)
    else:
        # 分片，保存本地
        file_path = os.path.join(
            app_settings.TMP_UPLOAD_DIR,
            file_info.file_id,
            file_info.chunk)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as fd:
            fd.write(file_obj.file.read())
        return Response()


def post_upload_success_request(request, file_info, app_settings):
    """ 合并文件的请求（所有分片均上传完后被调用）

    :param request: Request
    :param FileInfo file_info: 文件信息
    :param app_settings: settings
    :return: Response
    """
    dir_path = os.path.join(app_settings.TMP_UPLOAD_DIR, file_info.file_id)
    if not (os.path.exists(dir_path) and os.path.isdir(dir_path)):
        raise ValidationError('分片文件不存在')
    file_path = os.path.join(dir_path, file_info.file_name)
    try:
        with open(file_path, 'ab') as fd:
            chunk = 0  # 分片序号
            while True:
                chunk_file_path = os.path.join(dir_path, chunk)
                if os.path.exists(chunk_file_path) and os.path.isfile(
                        chunk_file_path):
                    with open(chunk_file_path, 'rb') as chunk_fd:
                        fd.write(chunk_fd.read())
                    chunk += 1
                else:
                    break
        with open(file_path, 'ab') as fd:
            data = __upload(request, file_info, fd, app_settings)
        return Response(data=data)
    except BaseException:
        raise ValidationError('文件合并错误')
    finally:
        shutil.rmtree(dir_path)


class UploadBaseView:
    api_settings = None

    def get_api_settings(self):
        assert self.api_settings is not None, (
            "'%s' should either include a `api_settings` attribute, "
            "or override the `get_api_settings()` method."
            % self.__class__.__name__
        )
        return self.api_settings


class UploadView(UploadBaseView):

    def post(self, request, *args, **kwargs):
        file_info = FileInfo(file_type=request.data['type'],
                             file_id=request.data['uuid'],
                             dir_path=f"{request.data['type']}/{request.data['task_id']}",
                             task_id=request.data['task_id'],
                             chunk=request.data.get('chunk', -1),
                             file_name=None)
        file_obj = request.data['file']
        return post_upload_request(
            request, file_info, file_obj, self.get_api_settings())


class UploadSuccessView(UploadBaseView):

    def post(self, request, *args, **kwargs):
        file_info = FileInfo(file_type=request.data['type'],
                             file_id=request.data['uuid'],
                             dir_path=f"{request.data['type']}/{request.data['task_id']}",
                             task_id=request.data['task_id'],
                             chunk=None,
                             file_name=request.data['filename'])
        return post_upload_success_request(
            request, file_info, self.get_api_settings())
