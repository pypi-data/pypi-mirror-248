#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from django.contrib.auth import password_validation
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator

from rest_framework_util.serializers import BaseSwitchModelSerializer, BaseModelSerializer, RelatedUserModelSerializer
from rest_framework_admin.user.models import User, Group, UserGroupRel


def _get_related_role_model_serializer():
    from rest_framework_admin.role.serializers import RelatedRoleSubjectRelModelSerializer
    return RelatedRoleSubjectRelModelSerializer


class UserModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    username = serializers.CharField(
        help_text='账户（不允许更新）',
        validators=(
            UniqueValidator(
                queryset=User.objects.filter()),))
    password = serializers.CharField(
        help_text='密码（不允许更新）',
        write_only=True, validators=[
            password_validation.validate_password])
    is_staff = serializers.BooleanField(
        required=False,
        default=True,
        help_text='是否为员工，默认为True')
    is_active = serializers.BooleanField(
        required=False,
        default=True,
        help_text='是否激活，默认为True')
    is_superuser = serializers.BooleanField(
        required=False,
        default=False,
        help_text='是否为超级用户，默认为False')
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, help_text='描述')
    telephone = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, help_text='电话')
    role = serializers.SerializerMethodField()
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='真实姓名')
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='昵称')
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='邮箱')
    # avatar = ImageOrCharField(
    #     max_length=256,
    #     required=False,
    #     allow_blank=True,
    #     allow_null=True)

    class Meta:
        model = User
        read_only_fields = ('create_datetime', 'id', 'last_login')
        exclude = ('delete_user', 'delete_datetime')

    @staticmethod
    def save_user_role(user, role, create_user_id):
        from role.models import RoleSubjectRel
        from role.configs import SubjectTypeEnum
        is_role_exists = user.filter_roles().filter(pk=role.id).exists()
        if is_role_exists:
            rel = RoleSubjectRel.objects.get(
                role_id=role.id,
                subject_id=user.id,
                subject_type=SubjectTypeEnum.user.name
            )
            if rel.expire_ts is not None:
                rel.expire_ts = None
                rel.update_user_id = create_user_id
                rel.save()
            return
        user.save_roles(role.id, create_user_id=create_user_id)

    def create(self, validated_data):
        validated_data['name'] = validated_data['username']
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        from role.models import Role
        from role.configs import DefaultRoleEnum
        role = Role.objects.get(pk=DefaultRoleEnum.visitor.value)
        self.save_user_role(user, role, validated_data['create_user_id'])
        return user

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        return instance

    @extend_schema_field(_get_related_role_model_serializer())
    def get_role(self, obj):
        rel = obj.get_max_role_rel()
        if rel is not None:
            return _get_related_role_model_serializer()(
                instance=rel, context=self.context).data
        return rel


class SwitchUserModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = User


class UpdatePasswordUserModelSerializer(serializers.ModelSerializer):
    """ 用户更新密码 """
    old_password = serializers.CharField(help_text='旧密码', write_only=True)
    new_password = serializers.CharField(
        help_text='新密码',
        write_only=True, validators=[
            password_validation.validate_password])

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError(_('密码错误，请确认'))
        return value

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        instance = super().update(instance, validated_data)
        return instance


class UpdateUserPasswordUserModelSerializer(serializers.ModelSerializer):
    """ 更新用户密码 """
    new_password = serializers.CharField(
        help_text='新密码',
        write_only=True, validators=[
            password_validation.validate_password])

    class Meta:
        model = User
        fields = ('new_password', )

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        instance.set_password(new_password)
        instance = super().update(instance, validated_data)
        return instance


class SelectionUserModelSerializer(RelatedUserModelSerializer):

    class Meta(RelatedUserModelSerializer.Meta):
        pass


class UserRelatedGroupModelSerializer(
        BaseModelSerializer, serializers.ModelSerializer):
    id = serializers.CharField(source='group_id', read_only=True)
    name = serializers.CharField(source='group__name', read_only=True)
    group_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=Group.objects.all()))

    class Meta:
        model = UserGroupRel
        fields = ('id', 'name', 'create_datetime', 'create_user', 'group_ids')
        read_only_fields = ('id', 'name', 'create_datetime', 'create_user')

    def create(self, validated_data):
        for group in validated_data.pop('group_ids'):
            if not UserGroupRel.objects.filter(
                    group_id=group.id,
                    user_id=validated_data['user_id']).exists():
                validated_data['group_id'] = group.id
                instance = super().create(validated_data)
        return instance


# =========== 组管理 ===========


class GroupModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=64, validators=[
            UniqueValidator(
                queryset=Group.objects.filter())])
    user_count = serializers.IntegerField(
        help_text='用户个数', read_only=True)
    expire_ts = serializers.SerializerMethodField()
    expire_datetime = serializers.DateTimeField(
        input_formats='%Y%m%d%H%M', required=False)

    class Meta(BaseModelSerializer.Meta):
        model = Group
        fields = BaseModelSerializer.Meta.fields + \
                 ('user_count', 'expire_datetime', 'expire_ts')

    @extend_schema_field(OpenApiTypes.INT)
    def get_expire_ts(self, obj):
        return self.get_ts_by_field(obj, 'expire_datetime')


class RelatedGroupModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'description')


class SwitchGroupModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = Group


class SelectionGroupModelSerializer(RelatedGroupModelSerializer):

    class Meta(RelatedGroupModelSerializer.Meta):
        pass


class GroupRelatedUserModelSerializer(
        BaseModelSerializer, serializers.ModelSerializer):
    id = serializers.CharField(source='user_id')
    name = serializers.CharField(source='user__username')
    user_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()))

    class Meta:
        model = UserGroupRel
        fields = ('id', 'name', 'create_datetime', 'create_user', 'user_ids')
        read_only_fields = ('id', 'name', 'create_datetime', 'create_user')

    def create(self, validated_data):
        for user in validated_data.pop('user_ids'):
            if not UserGroupRel.objects.filter(
                    user_id=user.id,
                    group_id=validated_data['group_id']).exists():
                validated_data['user_id'] = user.id
                instance = super().create(validated_data)
        return instance
