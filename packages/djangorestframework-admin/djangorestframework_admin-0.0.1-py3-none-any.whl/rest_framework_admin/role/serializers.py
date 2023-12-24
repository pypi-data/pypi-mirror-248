#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/17
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['RelatedRoleSubjectRelModelSerializer',
           'RoleModelSerializer',
           'SwitchRoleModelSerializer',
           'RoleRelatedPermissionModelSerializer',
           'SubjectListSerializer']

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework_admin.serializers import RelatedUserModelSerializer, BaseSwitchModelSerializer, BaseModelSerializer
from permission.models import Permission
from role.configs import RoleTypeEnum, SubjectTypeEnum
from role.models import Role, RolePermissionRel, RoleSubjectRel
from user.models import Group, User


class RoleModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    type = serializers.ChoiceField(
        [RoleTypeEnum.custom.name])
    name = serializers.CharField(max_length=64)
    code = serializers.CharField(max_length=64)
    subject_count = serializers.SerializerMethodField(help_text='主体个数统计')
    weight = serializers.IntegerField(
        required=False,
        help_text='权重，值越高优先级越高，即权限越大',
        min_value=1,
        max_value=100)

    class Meta(BaseModelSerializer.Meta):
        model = Role
        fields = BaseModelSerializer.Meta.fields + \
            ('code', 'subject_count', 'type', 'weight')
        validators = []

    @extend_schema_field({'type': 'object',
                          'properties': {'all': {'type': 'int',
                                                 'description': '所有主体个数'},
                                         '{key}': {'type': 'int',
                                                   'description': '个数,{key}为主体类型'}}})
    def get_subject_count(self, obj):
        data = {'all': obj.subject_rels.count()}
        for enum in SubjectTypeEnum:
            data[enum.name] = obj.subject_rels.filter(
                subject_type=enum.name).count()
        return data


class RelatedRoleSubjectRelModelSerializer(serializers.ModelSerializer):
    """ 关联的角色 """
    id = serializers.CharField(source='role_id', read_only=True)
    code = serializers.SlugRelatedField(
        source='role', slug_field='code', read_only=True)
    name = serializers.SlugRelatedField(
        source='role', slug_field='name', read_only=True)
    create_user = RelatedUserModelSerializer(help_text='绑定用户与角色的人员')

    class Meta:
        model = RoleSubjectRel
        fields = ('id', 'code', 'name', 'create_user', 'create_datetime')


class SwitchRoleModelSerializer(BaseSwitchModelSerializer):

    class Meta(BaseSwitchModelSerializer.Meta):
        model = Role


class SelectionRoleModelSerializer(BaseModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'type')


class RoleRelatedPermissionModelSerializer(
        BaseModelSerializer, serializers.ModelSerializer):
    id = serializers.CharField(source='permission_id')
    name = serializers.CharField(source='permission__name')
    permission_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all()))

    class Meta:
        model = RolePermissionRel
        fields = (
            'id',
            'name',
            'create_datetime',
            'create_user',
            'permission_ids')
        read_only_fields = ('id', 'name', 'create_datetime', 'create_user')

    def create(self, validated_data):
        for permission in validated_data.pop('permission_ids'):
            if not RolePermissionRel.objects.filter(
                    permission_id=permission.id,
                    role_id=validated_data['role_id']).exists():
                validated_data['permission_id'] = permission.id
                instance = super().create(validated_data)
        return instance


class RoleRelatedSubjectModelSerializer(
        BaseModelSerializer, serializers.ModelSerializer):
    id = serializers.CharField(source='subject_id')
    type = serializers.ChoiceField(
        [enum.name for enum in SubjectTypeEnum], source='subject_type')
    name = serializers.SerializerMethodField()
    subject_ids = serializers.ListField(
        min_length=1,
        max_length=10,
        write_only=True,
        child=serializers.CharField(max_length=32, min_length=32))

    class Meta:
        model = RoleSubjectRel
        fields = (
            'id',
            'type',
            'name',
            'create_datetime',
            'create_user',
            'subject_ids')
        read_only_fields = (
            'id',
            'name',
            'create_datetime',
            'create_user')

    def get_name(self, obj):
        return obj.subject.name

    def create(self, validated_data):
        subject_type = validated_data['type']
        for subject_id in validated_data.pop('subject_ids'):
            if subject_type == SubjectTypeEnum.group.name:
                enum = SubjectTypeEnum.group
                model = Group
            else:
                enum = SubjectTypeEnum.user
                model = User
            if not model.objects.filter(pk=subject_id).exists():
                raise ValidationError(
                    _(f'[{enum.value}]类型实体[id={subject_id}]不存在'))
            if not RoleSubjectRel.objects.filter(
                    subject_id=subject_id,
                    subject_type=subject_type,
                    role_id=validated_data['role_id']).exists():
                validated_data['subject_id'] = subject_id
                instance = super().create(validated_data)
        return instance


# ========== 主体 ==========


class SubjectListSerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    type = serializers.CharField()
    create_ts = serializers.SerializerMethodField()
    #
    username = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    last_login_ts = serializers.SerializerMethodField()
    expire_ts = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    #
    name = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    create_datetime = serializers.DateTimeField()

    class Meta:
        fields = list(set([
            'id',
            'type',

            # user类型
            'username',
            'nickname',
            'is_active',
            'last_login',
            'last_login_ts',
            'expire_ts'
            'description',

            # group类型
            'name',
            'description',
            'user_count',
            'create_ts']))

    def __get_obj(self, obj):
        key = '_obj_instance__'
        if key not in obj:
            if obj["type"] == SubjectTypeEnum.user.name:
                model = User
            else:
                model = Group
            obj[key] = model.objects.get(pk=obj["id"])
        return obj[key]

    def get_create_ts(self, obj):
        instance = self.__get_obj(obj)
        return BaseModelSerializer().get_create_ts(instance)

    def get_username(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'username', None)

    def get_name(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'name', None)

    def get_nickname(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'nickname', None)

    def get_last_login(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'last_login', None)

    def get_last_login_ts(self, obj):
        instance = self.__get_obj(obj)
        return BaseModelSerializer().get_ts_by_field(instance, 'last_login')

    def get_user_count(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'user_count', None)

    def get_expire_ts(self, obj):
        instance = self.__get_obj(obj)
        return getattr(instance, 'expire_ts', None)

    def get_role(self, obj):
        from user.serializers import UserModelSerializer
        instance = self.__get_obj(obj)
        if obj['type'] == SubjectTypeEnum.user.name:
            return UserModelSerializer(context=self.context).get_role(instance)
        return None
