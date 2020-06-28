# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class UserProfile(AbstractUser):
    """
    自定义的用户Model
    扩展字段：gender、nick_name、mobile、qq、wechart、dingding
    """

    GENDER_CHOICES = (
        ('male', "男"),
        ('female', "女"),
        ('secret', "保密")
    )
    nick_name = models.CharField(max_length=40, blank=True, verbose_name="昵称")
    # 头像url
    avater = models.CharField(verbose_name="头像", blank=True, null=True, max_length=256)
    gender = models.CharField(verbose_name="性别", max_length=6, choices=GENDER_CHOICES, default="secret")
    # email可以随便填写，但是手机号需要唯一：后续可加入校验验证码
    mobile = models.CharField(verbose_name="手机号", max_length=11, unique=True)
    qq = models.CharField(max_length=12, verbose_name="QQ号", blank=True, null=True)
    # 公司有时候会用到钉钉/微信发送消息，需要记录用户相关ID
    dingding = models.CharField(max_length=40, verbose_name="钉钉ID", blank=True, null=True)
    wechart = models.CharField(max_length=40, verbose_name="微信ID", blank=True, null=True)
    # 能否访问本系统，默认是不可以访问本系统
    # 注意第一个管理员用户，可以去数据库调整can_view的值为1
    can_view = models.BooleanField(verbose_name="能访问", default=False, blank=True)
    is_deleted = models.BooleanField(verbose_name="删除", default=False, blank=True)

    def __repr__(self):
        return "UserProfile:{}".format(self.username)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

        permissions = (
            ("reset_password", "重置密码"),
        )


# 注意：get_user_model()方法可以获取到本系统使用的是哪个用户Model
# 默认的用户Model是：django.contrib.auth.models.User
# 在settings.py中配置：AUTH_USER_MODEL可以修改成指定的用户Model
# AUTH_USER_MODEL = "account.UserProfile"
User = get_user_model()
# 注意这句是要放在class UserProfile后面的
