import datetime

from django.db import models

# Create your models here.
from django.db.models import Value, CharField, Q
from django.utils import timezone

from rest_framework_admin.db.models.base import BaseModel
from permission.models import Permission
from role.configs import SubjectTypeEnum
from user.models import Group, User


class Role(BaseModel):
    code = models.CharField('编码', max_length=64)
    type = models.CharField('类型', max_length=32)
    weight = models.PositiveSmallIntegerField(
        '权重，值越高优先级越高，即权限越大')
    permissions = models.ManyToManyField(
        Permission, through='RolePermissionRel', through_fields=(
            'role', 'permission'), related_name='roles')

    class Meta:
        db_table = 'iam_role'
        verbose_name = '角色表'

    def __str__(self):
        return f'Role(id={self.id}, code={self.code}, type={self.type}, weight={self.weight})'

    @staticmethod
    def filter_by_subject(subject_id, subject_type, is_valid=None):
        """ 过滤直接绑定的角色 """
        queryset = Role.objects.filter(
            subject_rels__subject_id=subject_id,
            subject_rels__subject_type=subject_type)
        queryset = queryset.annotate(
            subject_id=Value(
                subject_id,
                output_field=CharField(
                    max_length=32)),
            subject_type=Value(subject_type, output_field=CharField(max_length=32)))
        if is_valid is None:
            return queryset
        if is_valid:
            queryset = queryset.filter(Q(subject_rels__expire_datetime__isnull=True) | Q(
                subject_rels__expire_datetime__lt=timezone.now()))
        else:
            queryset = queryset.exclude(
                subject_rels__expire_datetime__isnull=True).filter(
                subject_rels__expire_datetime__gte=timezone.now())
        return queryset

    @staticmethod
    def filter_by_valid(queryset, is_valid):
        if is_valid is None:
            return queryset
        if is_valid:
            queryset = queryset.filter(Q(expire_datetime__isnull=True) | Q(
                expire_datetime__lt=timezone.now()))
        else:
            queryset = queryset.exclude(
                expire_datetime__isnull=True).filter(
                expire_datetime__gte=timezone.now())
        return queryset

    def filter_users(self, is_valid=None):
        queryset = self.subject_rels.filter(
            subject_type=SubjectTypeEnum.user.name)
        queryset = self.filter_by_valid(queryset, is_valid)
        return User.objects.filter(
            id__in=queryset.values_list('subject_id', flat=True))

    def filter_groups(self, is_valid=None):
        queryset = self.subject_rels.filter(
            subject_type=SubjectTypeEnum.group.name)
        queryset = self.filter_by_valid(queryset, is_valid)
        return Group.objects.filter(
            id__in=queryset.values_list('subject_id', flat=True))

    def save_users(self, user_ids, **kwargs):
        return RoleSubjectRel.save_by_role(
            self.id, user_ids, SubjectTypeEnum.user.name, **kwargs)

    def save_groups(self, group_ids, **kwargs):
        return RoleSubjectRel.save_by_role(
            self.id, group_ids, SubjectTypeEnum.group.name, **kwargs)

    def delete_users(self, user_ids=None):
        return RoleSubjectRel.delete_by_role(
            self.id, user_ids, SubjectTypeEnum.user.name)

    def delete_groups(self, group_ids=None):
        return RoleSubjectRel.delete_by_role(
            self.id, group_ids, SubjectTypeEnum.group.name)


class RolePermissionRel(BaseModel):
    role = models.ForeignKey(Role, models.RESTRICT)
    permission = models.ForeignKey(Permission, models.RESTRICT)

    class Meta:
        db_table = 'iam_role_permission_rel'
        verbose_name = '角色权限关联表'
        unique_together = ('role', 'permission')

    def __str__(self):
        return f'RolePermissionRel(id={self.id}, role={self.role.id}, permission={self.permission.id})'


class RoleSubjectRel(BaseModel):
    subject_id = models.CharField(help_text='主体id，用户id/组id', max_length=32)
    role = models.ForeignKey(
        Role,
        models.RESTRICT,
        related_name='subject_rels')
    subject_type = models.CharField(help_text='主体类型，用户/组', max_length=32)
    expire_datetime = models.DateTimeField('过期时间', blank=True, null=True)

    class Meta:
        db_table = 'iam_role_subject_rel'
        verbose_name = '角色主体表'
        unique_together = ('subject_id', 'role', 'subject_type')

    def __str__(self):
        return f'RoleSubjectRel(id={self.id}, role={self.role.id}, subject_id={self.subject_id}, subject_type={self.subject_type})'

    @property
    def subject(self):
        if self.subject_type == SubjectTypeEnum.group.name:
            return Group.objects.get(pk=self.subject_id)
        else:
            return User.objects.get(pk=self.subject_id)

    @classmethod
    def save_by_role(cls, role_id, subject_ids, subject_type, **kwargs):
        if not isinstance(subject_ids, (tuple, list)):
            subject_ids = [subject_ids]
        for subject_id in subject_ids:
            kwargs['role_id'] = role_id
            kwargs['subject_id'] = subject_id
            kwargs['subject_type'] = subject_type
            rel = cls(**kwargs)
            rel.save()

    @classmethod
    def save_by_subject(cls, subject_id, role_ids, subject_type, **kwargs):
        if not isinstance(role_ids, (tuple, list)):
            role_ids = [role_ids]
        for role_id in role_ids:
            kwargs['role_id'] = role_id
            kwargs['subject_id'] = subject_id
            kwargs['subject_type'] = subject_type
            rel = cls(**kwargs)
            rel.save()

    @classmethod
    def delete_by_role(cls, role_id, subject_ids, subject_type):
        kwargs = {
            'subject_type': subject_type,
            'role_id': role_id
        }
        if subject_ids is None:
            cls.objects.filter(**kwargs).delete()
            return
        if not isinstance(subject_ids, (tuple, list)):
            subject_ids = [subject_ids]
            kwargs['subject_id__in'] = subject_ids
        cls.objects.filter(**kwargs).delete()

    @classmethod
    def delete_by_subject(cls, subject_id, role_ids, subject_type):
        kwargs = {
            'subject_type': subject_type,
            'subject_id': subject_id
        }
        if role_ids is None:
            cls.objects.filter(**kwargs).delete()
            return
        if not isinstance(role_ids, (tuple, list)):
            role_ids = [role_ids]
            kwargs['role_id__in'] = role_ids
        cls.objects.filter(**kwargs).delete()
