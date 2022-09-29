# -*- coding:utf-8 -*-
from django.db import models

from codelieche.django.models import BaseModel
from account.models.system import System


class Permission(BaseModel):
    """系统权限"""
    delete_update_fields = ("code",)

    system = models.ForeignKey(verbose_name="系统模块", to=System, to_field="code", on_delete=models.CASCADE,
                               related_name="permissions")
    code = models.CharField(verbose_name="权限代码", max_length=128)
    name = models.CharField(verbose_name="权限名称", max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="权限描述", max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name
        unique_together = ("system", "code")

