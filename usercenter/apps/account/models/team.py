# -*- coding:utf-8 -*-
"""
添加新的团队的时候我们默认创建项目角色
1. user: 普通用户
2. develop: 开发人员
3. test: 测试人员
4. pm: 产品经理
5. devops: 运维人员
6. admin: 管理员
在序列化的create方法中调用team_create_signal的call方法
"""
from django.db import models
from codelieche.django.models import BaseModel


class Team(BaseModel):
    """
    团队/分组
    """
    delete_tasks = ("delete_project_roles",)
    delete_update_fields = ("name",)
    # code是只可修改一次，如果未传入可设置个随机字符
    code = models.CharField(verbose_name="团队代码", max_length=128, unique=True)
    name = models.CharField(verbose_name="团队名称", max_length=128, db_index=True)
    users = models.ManyToManyField(verbose_name="用户", to="User", blank=True)
    owner = models.ForeignKey(verbose_name="拥有者", blank=True, null=True,
                              to="User", on_delete=models.CASCADE, related_name="owner")
    logo = models.CharField(verbose_name="Logo", max_length=256, blank=True, null=True)
    description = models.TextField(verbose_name="描述", blank=True, null=True)
    # 团队的配置项：比如第三方登录、LDAP、邮箱配置等都可放入这里面
    config = models.JSONField(verbose_name="配置", blank=True, null=True)
    # 状态
    is_active = models.BooleanField(verbose_name="状态", blank=True, default=True)

    def delete_project_roles(self):
        # 1. 获取到项目角色列表queryset
        project_roles = self.get_relative_object_by_content_type(
            app_label="account", model="projectrole", many=True,
            value=self.id, field="team_id",
        )
        # 2. 如果有值，就执行删除操作
        if project_roles:
            for role in project_roles:
                role.delete()
            # 直接执行queryset的delete()就是物理删除了
            # project_roles.delete()

    class Meta:
        verbose_name = "团队"
        verbose_name_plural = verbose_name
