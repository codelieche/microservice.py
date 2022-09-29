# -*- coding:utf-8 -*-
from django.db import models
from codelieche.django.models import BaseModel

from account.models.team import Team
from account.models.system import System
from account.models.permission import Permission


class Role(BaseModel):
    """
    团队的角色/系统默认的角色
    """
    delete_update_fields = ("code",)

    system = models.ForeignKey(verbose_name="系统", to=System, blank=True, null=True, on_delete=models.CASCADE)
    # 团队和角色code应该是联合唯一
    team = models.ForeignKey(verbose_name="团队", to=Team, blank=True, null=True, on_delete=models.CASCADE)
    code = models.CharField(verbose_name="角色代码", max_length=128, db_index=True)
    name = models.CharField(verbose_name="角色名称", max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    permissions = models.ManyToManyField(verbose_name="权限", to=Permission, blank=True)

    @property
    def team_name(self):
        if self.team:
            return self.team.name
        else:
            return None

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

        # unique_together = ("system", "team", "code")
