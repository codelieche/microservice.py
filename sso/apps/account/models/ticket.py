# -*- coding:utf-8 -*-
from django.db import models

from account.models.user import User


class Ticket(models.Model):
    """
    登录券
    """
    user = models.ForeignKey(to=User, verbose_name="用户", on_delete=models.CASCADE)
    sessionid = models.CharField(verbose_name="Session ID", max_length=128)
    name = models.BigIntegerField(verbose_name="券名字", unique=True)
    return_url = models.CharField(verbose_name="跳转地址", max_length=256)
    time_added = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True)
    time_expired = models.DateTimeField(verbose_name="过期时间", blank=True, null=True)
    is_active = models.BooleanField(verbose_name="是否有效", blank=True, default=False)

    class Meta:
        verbose_name = "登录券"
        verbose_name_plural = verbose_name
