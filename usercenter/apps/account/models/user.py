# -*- coding:utf-8 -*-
import datetime

import jwt
from passlib.hash import pbkdf2_sha256
from django.utils import timezone
from django.db import models
from django.conf import settings

from .role import Role
from account.models.permission import Permission


class AnonymousUser:
    """匿名用户"""
    username = ''
    is_authenticated = False


class User(models.Model):
    """
    自定义的用户Model
    """
    GENDER_CHOICES = (
        ('male', "男"),
        ('female', "女"),
        ('secret', "保密")
    )
    username = models.CharField(verbose_name="用户名", max_length=60, unique=True)
    password = models.CharField(verbose_name="密码", max_length=256, blank=True)
    email = models.EmailField(verbose_name="邮箱", max_length=128, blank=True, null=True)
    is_active = models.BooleanField(verbose_name="激活", blank=True, default=True)
    is_superuser = models.BooleanField(verbose_name="超级用户", blank=True, default=False)
    is_staff = models.BooleanField(verbose_name="可登录admin", blank=True, default=False)

    nick_name = models.CharField(max_length=60, blank=True, verbose_name="昵称")
    # 头像url
    avatar = models.CharField(verbose_name="头像", blank=True, null=True, max_length=256)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="secret", verbose_name="性别")
    # email可以随便填，但是手机号需要唯一: 后续可加入校验验证码
    # 开始创建用户的时候，如果phone为空，可以让其先等于username
    phone = models.CharField(max_length=11, verbose_name="手机号", unique=True)
    # 能否访问本系统，默认是不可以访问本系统
    # 注意第一个管理员用户，可以去数据库调整can_view的值为1
    can_view = models.BooleanField(verbose_name="能访问", default=False, blank=True)
    is_deleted = models.BooleanField(verbose_name="删除", default=False, blank=True)

    # 设置角色
    roles = models.ManyToManyField(verbose_name="角色", to=Role, blank=True)

    def __repr__(self):
        return "User:{}".format(self.username)

    def __str__(self):
        return self.username

    @property
    def team_id(self):
        if hasattr(self, '_team_id'):
            return self._team_id
        else:
            team = self.team_set.filter(deleted=False).first()
            if team:
                self._team_id = team.id
                return team.id
            return None

    @team_id.setter
    def team_id(self, team_id):
        team = self.team_set.filter(id=team_id).first()
        if team:
            # self._team_id = team.id
            setattr(self, '_team_id', team.id)
        else:
            self._team_id = team.id
            setattr(self, '_team_id', None)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 1. 校验密码
        if self.password and self.password.find('$pbkdf2-sha256') != 0:
            self.set_password(password=self.password)

        # 调用父方法
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def set_password(self, password):
        if password:
            self.password = pbkdf2_sha256.hash(password)
        else:
            raise ValueError('传入的密码为空:{}'.format(password))

    def check_password(self, password):
        try:
            return pbkdf2_sha256.verify(password, self.password)
        except Exception as e:
            print('校验密码出错：{}'.format(e))
            # if self.password and password:
            #     return self.password == password
            return False

    def generate_jwt_token(self, seconds=3600*12):
        now = datetime.datetime.now(tz=timezone.utc)
        expired = now + datetime.timedelta(seconds=seconds)
        data = {
            'exp': expired,
            'nbf': now - datetime.timedelta(seconds=60),
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
        }
        secret = settings.JWT_SECRET
        token = jwt.encode(data, secret, algorithm='HS256')
        return token

    @classmethod
    def decode_jwt_token(cls, token):
        try:
            data = jwt.decode(
                token, key=settings.JWT_SECRET, algorithms=['HS256'],
                # options={"verify_signature": False}  # 如果加入这个参数，就不验证secret了
            )
            return True, data
        except Exception as e:
            return False, e

    @property
    def is_authenticated(self):
        return self.is_active and self.username != ""

    def get_permissions(self):
        """获取用户的所有权限列表"""
        # 1. 先获取到用户的角色
        roles_id_list = tuple(self.roles.values_list('id', flat=True))
        if not roles_id_list:
            return []

        # 2. 获取到所有的权限的id
        permission_table = Permission.objects.model._meta.db_table
        sql = "select * from {} WHERE  deleted=0 AND " \
              "id in (select permission_id from account_role_permissions where role_id in {})".\
            format(permission_table, str(roles_id_list).replace(",)", ")"))
        # print(sql)
        permissions = Permission.objects.raw(sql)

        # 3. 返回权限
        return permissions


