#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/21
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from django.db import migrations

from role.configs import DefaultRoleEnum
from user.configs import DefaultUserEnum


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    RoleSubjectRel = apps.get_model("role", "RoleSubjectRel")
    db_alias = schema_editor.connection.alias
    RoleSubjectRel.objects.using(db_alias).bulk_create(
        [
            RoleSubjectRel(
                subject_id=DefaultUserEnum.admin.value,
                subject_type='user',
                role_id=DefaultRoleEnum.admin.value,
                create_user_id=DefaultUserEnum.root.value),
            RoleSubjectRel(
                subject_id=DefaultUserEnum.test.value,
                subject_type='user',
                role_id=DefaultRoleEnum.visitor.value,
                create_user_id=DefaultUserEnum.root.value),
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_create_user'),
        ('role', '0002_create_role'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
