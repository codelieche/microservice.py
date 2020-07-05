# -*- coding:utf-8 -*-
import json

from django.db import models
from django.utils.encoding import force_text
from django.utils import timezone

# Create your models here.


class Service(models.Model):
    """
    服务
    """
    name = models.CharField(verbose_name="服务名", max_length=60)
    code = models.CharField(verbose_name="服务代码", max_length=40, unique=True)
    description = models.CharField(verbose_name="描述", blank=True, max_length=512, null=True)
    is_active = models.BooleanField(verbose_name="启用", blank=True, default=True)

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name


class ModelLog(models.Model):
    """
    模型对象的日志
    """
    ACTION_FLAG_CHOICES = (
        (1, "添加"),
        (2, "修改"),
        (3, "删除")
    )
    user = models.CharField(verbose_name="用户", max_length=60, blank=True, null=True)
    service = models.CharField(verbose_name="服务", max_length=60, db_index=True)
    model = models.CharField(verbose_name="模型", max_length=40, db_index=True)
    object_id = models.BigIntegerField(verbose_name="对象ID", db_index=True)
    object_repr = models.CharField(verbose_name="对象", max_length=200, blank=True)
    # 操作标志
    action_flag = models.PositiveSmallIntegerField(verbose_name="操作标志", choices=ACTION_FLAG_CHOICES)
    # 操作的消息内容
    content = models.TextField(verbose_name="消息内容", blank=True)
    # 添加日期
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)
    # 是否删除
    is_deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)

    # 使用自定义的管理器

    class Meta:
        verbose_name = "Model日志"
        verbose_name_plural = verbose_name
        ordering = ("-time_added",)

    def __repr__(self):
        return force_text(self.time_added)

    def __str__(self):
        return force_text(self.time_added)
