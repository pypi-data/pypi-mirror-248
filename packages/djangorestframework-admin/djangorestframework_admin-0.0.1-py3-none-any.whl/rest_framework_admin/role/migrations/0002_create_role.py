#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

""" 创建角色 """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from django.db import migrations

from role.configs import DefaultRoleEnum
from user.configs import DefaultUserEnum


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Role = apps.get_model("role", "Role")
    db_alias = schema_editor.connection.alias
    Role.objects.using(db_alias).bulk_create(
        [
            Role(
                id=DefaultRoleEnum.admin.value,
                code=DefaultRoleEnum.admin.name,
                type='builtin',
                name='管理员',
                weight=100,
                create_user_id=DefaultUserEnum.root.value),
            Role(
                id=DefaultRoleEnum.visitor.value,
                code=DefaultRoleEnum.visitor.name,
                type='builtin',
                name='访客',
                weight=0,
                create_user_id=DefaultUserEnum.root.value),
        ]
    )


def reverse_func(apps, schema_editor):
    Role = apps.get_model("role", "Role")
    db_alias = schema_editor.connection.alias
    Role.objects.using(db_alias).filter(
        id=DefaultRoleEnum.admin.value).delete()
    Role.objects.using(db_alias).filter(
        id=DefaultRoleEnum.visitor.value).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
        ('user', '0002_create_user')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
