# -*- coding:utf-8 -*-
"""
Team Model Signal
"""
from django.dispatch import receiver, Signal

from account.models.team import Team
from account.models.project import ProjectRole

team_create_signal = Signal()


@receiver(signal=team_create_signal)
def team_created_create_role(sender, **kwargs):
    if isinstance(sender, Team):
        # 创建系统默认的几个角色
        roles = [
            {"code": "user", "name": "普通用户"},
            {"code": "develop", "name": "开发人员"},
            {"code": "test", "name": "测试人员"},
            {"code": "pm", "name": "产品经理"},
            {"code": "devops", "name": "运维人员"},
            {"code": "admin", "name": "管理员"},
        ]
        for item in roles:
            name = item['name']
            ProjectRole.objects.create(
                team=sender,
                code=item['code'],
                name=name,
                description=name,
            )
