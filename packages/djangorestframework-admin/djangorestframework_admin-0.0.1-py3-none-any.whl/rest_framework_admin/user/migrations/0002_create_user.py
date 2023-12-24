#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

""" 创建默认用户 """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import migrations

from user.configs import DefaultUserEnum


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    # User = apps.get_model("user", "User")
    User = get_user_model()
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).bulk_create(
        [
            User(
                id=DefaultUserEnum.root.value,
                username=DefaultUserEnum.root.name,
                password=make_password("root@2023"),
                nickname='超级管理员',
                is_staff=True,
                is_superuser=True),
            User(
                id=DefaultUserEnum.admin.value,
                username=DefaultUserEnum.admin.name,
                password=make_password("admin@2023"),
                nickname='管理员',
                is_staff=True,
                is_superuser=False),
            User(
                id=DefaultUserEnum.test.value,
                username=DefaultUserEnum.test.name,
                password=make_password("test@2023"),
                nickname='用户',
                is_staff=False,
                is_superuser=False),
        ]
    )


def reverse_func(apps, schema_editor):
    # so reverse_func() should delete them.
    # User = apps.get_model("user", "User")
    User = get_user_model()
    db_alias = schema_editor.connection.alias
    User.objects.using(db_alias).filter(id=DefaultUserEnum.root.value).delete()
    User.objects.using(db_alias).filter(
        id=DefaultUserEnum.admin.value).delete()
    User.objects.using(db_alias).filter(id=DefaultUserEnum.test.value).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial')
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
