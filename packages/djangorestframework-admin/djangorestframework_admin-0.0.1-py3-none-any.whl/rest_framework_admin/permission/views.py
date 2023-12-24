# Create your views here.
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets

from permission.filters import PermissionFilter
from permission.models import Permission
from permission.permissions import PermissionModelPermission
from permission.serializers import PermissionModelSerializer


@extend_schema_view()
class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """ 权限 """
    queryset = Permission.objects.filter().order_by('-create_datetime').all()
    serializer_class = PermissionModelSerializer
    filterset_class = PermissionFilter
    search_fields = ['name']
    ordering_fields = ['name', 'create_datetime']
    permission_classes = (PermissionModelPermission, )

    def perform_create(self, serializer):
        serializer.save(create_user_id=self.request.user.id)
