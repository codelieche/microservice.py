# -*- coding:utf-8 -*-
from django.db import models

from codelieche.django.models import BaseModel


class TodoList(BaseModel):
    delete_tasks = ['delete_task_change_title']
    title = models.CharField(verbose_name="标题", max_length=256, blank=True, null=True)
    done = models.BooleanField(verbose_name="已完成", blank=True, default=False)
    time_updated = models.DateTimeField(verbose_name="更新时间", blank=True, auto_now=True)
    time_finished = models.DateTimeField(verbose_name="完成时间", blank=True, null=True)

    def delete_task_change_title(self):
        self.title = "{}_{}".format(self.title, self.strftime())
        self.save()

    class Meta:
        verbose_name = "TodoList"
        verbose_name_plural = verbose_name
