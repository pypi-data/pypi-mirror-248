#!/usr/bin/python
# -*- coding:utf-8 -*-
# DateTime:2023/6/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['RefreshSerializer', 'TokenSerializer', 'OauthLogoutSerializer']

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from auth.jwt.configs import CookieEnum
from auth.jwt.exceptions import AuthVerifyError
from auth.jwt.utils import is_token_in_blacklist


class BlacklistRefreshToken(RefreshToken):
    def verify(self, *args, **kwargs) -> None:
        super().verify(*args, **kwargs)
        self.check_blacklist()

    def check_blacklist(self):
        if is_token_in_blacklist(self):
            raise TokenError(_("Token has no id"))


class RefreshSerializer(TokenRefreshSerializer):
    """
    调整 `refresh` 为非必填项，此时通过COOKIE获取
    """
    refresh = serializers.CharField(required=False, default=None)
    token_class = BlacklistRefreshToken

    def validate_refresh(self, value):
        if value is None:
            value = self.context['request'].COOKIES.get(
                CookieEnum.refresh.value, None)
        if not value:
            raise AuthVerifyError(_('没有refresh token'))
        return value


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            self.context['request'].user = self.user
            return data
        except exceptions.AuthenticationFailed as exc:
            raise AuthVerifyError(_('认证失败，未找到有效用户'))

    @classmethod
    def get_token_for_iam(cls, user, oauth_type=None):
        refresh = cls.get_token(user)
        refresh['oauth_type'] = oauth_type
        return refresh


class OauthLogoutSerializer(serializers.Serializer):
    grant_type = serializers.ChoiceField(choices=['logout'])
    refresh_token = serializers.CharField(max_length=256)
    client_id = serializers.CharField(max_length=256)
    client_secret = serializers.CharField(max_length=256)
