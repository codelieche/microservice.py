# -*- coding:utf-8 -*-
from django.db import models
from django.utils import timezone

from codelieche.django.utils import Cryptography


class BaseModel(models.Model):
    """
    基础Model类
    添加了deleted字段, 覆写了save方法
    """
    SECRET_FIELDS = ()  # 需要加密的字段

    # 字段：删除、添加时间
    deleted = models.BooleanField(verbose_name="删除", blank=True, default=False)
    time_added = models.DateTimeField(verbose_name="添加时间", blank=True, auto_now_add=True, null=True)

    @staticmethod
    def strftime(fmt='%Y%m%d%H%M%S'):
        """
        格式化当前的时间戳，删除资源的时候会用到
        """
        return timezone.datetime.now().strftime(fmt)

    def set_decrypt_value(self):
        # 加密存储的字段
        if self.SECRET_FIELDS and isinstance(self.SECRET_FIELDS, (list, tuple)):
            p = Cryptography()

            # 自己配置SECRET_FIELDS, BaseModel中默认是[]
            for i in self.SECRET_FIELDS:
                value = getattr(self, i)
                if i and value:
                    # 判断是否是加密的
                    success, _ = p.check_can_decrypt(value)
                    if not success:
                        setattr(self, i, p.encrypt(text=value))
            # 对需要加密的字段加密完毕

    def get_decrypt_value(self, field: str) -> str:
        """
        获取解密后的值
        """
        value = getattr(self, field)
        if value:
            p = Cryptography()
            success, de_p = p.check_can_decrypt(value=value)
            if success:
                return de_p
            else:
                return value

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 调用设置加密字段的方法
        self.set_decrypt_value()
        # 调用父类的save方法
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    class Meta:
        # 抽象类
        abstract = True
