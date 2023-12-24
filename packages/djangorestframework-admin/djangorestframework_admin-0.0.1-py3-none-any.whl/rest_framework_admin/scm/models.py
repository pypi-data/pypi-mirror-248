import json

from django.db import models

# Create your models here.
from rest_framework_admin.db.models.base import BaseModel


class Config(BaseModel):
    value = models.TextField('值', null=True, blank=True)

    class Meta:
        db_table = 'scm_config'
        verbose_name = '系统配置表'
