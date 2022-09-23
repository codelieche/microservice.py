# -*- coding:utf-8 -*-
from django.db import models

from codelieche.django.models import BaseModel


class Email(BaseModel):
    delete_tasks = ['delete_task_change_name']
    SECRET_FIELDS = ("password",)
    platform = models.CharField(verbose_name="平台", max_length=100, blank=True, null=True)
    name = models.CharField(verbose_name="有些名称", max_length=100)
    password = models.CharField(verbose_name="密码", max_length=256)

    def delete_task_change_name(self):
        self.name = "{}_{}".format(self.name, self.strftime())
        self.save()

    class Meta:
        verbose_name = "邮箱"
        verbose_name_plural = verbose_name
