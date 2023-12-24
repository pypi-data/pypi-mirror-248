from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from scm.filters import ConfigFilter
from scm.models import Config
from scm.permissions import ConfigPermission
from scm.serializers import ListConfigModelSerializer, UpdateConfigModelSerializer
from scm.settings import api_settings
from scm.utils import UploadView, UploadSuccessView


def get_user(request):
    return request.user


@extend_schema_view(
    get=extend_schema(
        summary='系统配置/列表', parameters=[
            OpenApiParameter('name', description='多个值英文逗号分隔')]),
    put=extend_schema(summary='系统配置/更新'),
    patch=extend_schema(summary='系统配置/更新')
)
class SysConfigAPIView(ListAPIView, UpdateAPIView):
    queryset = Config.objects.all()
    pagination_class = None
    serializer_class = ListConfigModelSerializer
    filterset_class = ConfigFilter
    search_fields = ['name']
    ordering_fields = ['name', 'create_datetime', 'update_datetime']
    ordering = ['-create_datetime']
    permission_classes = (ConfigPermission,)

    def get_serializer_class(self):
        if self.request.method != 'GET':
            return UpdateConfigModelSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user(self.request)
        serializer.save(update_user_id=user.id)
        return Response({})


@extend_schema_view(
    post=extend_schema(
        summary='文件/上传',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {'type': 'string', 'format': 'binary', 'description': '文件'},
                    'type': {'type': 'string', 'description': '类型'},
                    'uuid': {'type': 'string', 'description': '分片时，用于文件唯一标识；不分片就不用'},
                    'task_id': {'type': 'string', 'description': '文件id，用于生成文件夹名称'},
                    'chunk': {'type': 'int', 'description': '分片序号，-1表示部不分片'}
                },
                'required': ['file', 'type', 'uuid', 'task_id']
            }},
    ),
)
class UploadAPIView(UploadView, APIView):
    api_settings = api_settings


@extend_schema_view(
    post=extend_schema(
        summary='文件/合并（只针对分片上传的文件）',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'filename': {'type': 'string', 'description': '文件名称'},
                    'type': {'type': 'string', 'description': '类型'},
                    'uuid': {'type': 'string', 'description': '用于文件唯一标识'},
                    'task_id': {'type': 'string', 'description': '文件id，用于生成文件夹名称'}
                },
                'required': ['filename', 'type', 'uuid', 'task_id']
            }}, ),
)
class UploadSuccessAPIView(UploadSuccessView, APIView):
    api_settings = api_settings
