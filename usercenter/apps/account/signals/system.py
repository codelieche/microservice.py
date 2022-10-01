# -*- coding:utf-8 -*-
"""
System Model Signal
"""
from django.dispatch import receiver, Signal

from account.models.system import System
from account.models.role import Role

system_create_signal = Signal()


@receiver(signal=system_create_signal)
def system_created_create_role(sender, **kwargs):
    if isinstance(sender, System):
        # 创建系统默认的几个角色
        roles = [
            {"code": "default", "name": "默认"},
            {"code": "user", "name": "普通用户"},
            {"code": "admin", "name": "管理员"}
        ]
        for item in roles:
            name = "{}.{}".format(sender.name, item['name'])
            Role.objects.create(
                system=sender,
                code="{}.{}".format(sender.code, item['code']),
                name=name,
                description=name,
            )
