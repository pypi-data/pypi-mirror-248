# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from auth.serializers import AuthMeUserModelSerializer, RegisterUserModelSerializer


@extend_schema_view(
    get=extend_schema(summary='用户自查')
)
class AuthMeRetrieveAPIView(RetrieveAPIView):
    serializer_class = AuthMeUserModelSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(summary='用户注册')
)
class AuthRegisterCreateAPIView(CreateAPIView):
    serializer_class = RegisterUserModelSerializer
