# -*- coding:utf-8 -*-
"""
账号登录日志
"""
from django.db import models

from account.models.user import User


class SafeLog(models.Model):
    """
    账号安全日志
    1. 用户登录的时候记录：【成功/失败都记录】
    2. 用户修改密码的时候记录
    3. 重置密码的时候记录
    """
    CATEGORY_CHOICES = (
        ("default", "Default"),
        ("login", "登录"),
        ("safe", "安全"),
        ("other", "其它")
    )
    user = models.ForeignKey(to=User, verbose_name="用户", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name="操作IP")
    devices = models.CharField(verbose_name="操作设备", max_length=256, blank=True, null=True)
    category = models.CharField(verbose_name="类型", max_length=10, choices=CATEGORY_CHOICES, db_index=True,
                                blank=True, default="default")
    content = models.CharField(verbose_name="内容", max_length=256)
    success = models.BooleanField(verbose_name="是否成功", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        ordering = ("-id",)
