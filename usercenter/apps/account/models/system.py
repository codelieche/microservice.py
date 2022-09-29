# -*- coding:utf-8 -*-
"""
添加新的系统模块的时候我们默认创建3个系统角色
1. system.code.default: 系统默认
2. system.code.user: 系统普通用户
3. system.code.admin: 系统管理员
在序列化的create方法中调用system_create_signal的call方法
"""
from django.db import models
from codelieche.django.models import BaseModel


class System(BaseModel):
    """
    系统模块
    """

    # 删除的时候，自动修改的字段
    delete_update_fields = ('code',)

    code = models.SlugField(verbose_name="系统代码", max_length=60, unique=True)
    name = models.CharField(verbose_name="系统名称", max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=512, blank=True, null=True)

    class Meta:
        verbose_name = "系统模块"
        verbose_name_plural = verbose_name
