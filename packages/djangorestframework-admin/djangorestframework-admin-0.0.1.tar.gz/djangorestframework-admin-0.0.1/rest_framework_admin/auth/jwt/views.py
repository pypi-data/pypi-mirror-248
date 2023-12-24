# Create your views here.

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from auth.jwt.configs import CookieEnum, TokenEnum
from auth.jwt.utils import blacklist


@extend_schema_view(
    post=extend_schema(summary='登出', responses=OpenApiTypes.NONE)
)
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({})
        cookie_keys = [enum.value for enum in CookieEnum]
        for key in request.COOKIES.keys():
            if key in cookie_keys:
                response.delete_cookie(key)
        if not isinstance(request.user, AnonymousUser):
            blacklist.add_by_user(request.user)
        return response


class CookieAPIView:
    @classmethod
    def set_cookie(cls, request, response, data=None):
        data = data or response.data or {}
        cache_data = {}
        for token, cookie, method in (
                (TokenEnum.access.value, CookieEnum.access.value, AccessToken),
                (TokenEnum.refresh.value, CookieEnum.refresh.value, RefreshToken)):
            value = data.get(token, None)
            if value is not None:
                # max_age=60 * 60 * 24, httponly=True
                response.set_cookie(cookie, value)
            token_data = method(value)
            cache_data[token] = token_data.payload['jti']
        cache.set(request.user.id, cache_data)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if is_success(response.status_code):
            self.set_cookie(request, response)
        return response


@extend_schema_view(
    post=extend_schema(summary='登入')
)
class LoginAPIView(CookieAPIView, TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(summary='刷新token')
)
class RefreshAPIView(CookieAPIView, TokenRefreshView):
    pass
