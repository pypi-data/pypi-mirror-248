from django.db import models
from rest_framework_admin.db.models.base import BaseModel


class Permission(BaseModel):
    content_type = models.CharField('内容类型', max_length=64)
    action = models.CharField('动作', max_length=64)

    class Meta:
        db_table = 'iam_permission'
        verbose_name = '权限表'
        unique_together = ('content_type', 'action')

    def __str__(self):
        return f'Permission(id={self.id}, content_type={self.content_type}, action={self.action})'
