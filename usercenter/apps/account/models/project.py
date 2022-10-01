# -*- coding:utf-8 -*-
from django.db import models
from codelieche.django.models import BaseModel


class ProjectRole(BaseModel):
    """
    项目的角色
    不同团队自行设置自己的项目角色，后续很多的资源会与项目相绑定
    项目角色是团队全局的
    """
    delete_update_fields = ("code",)

    team = models.ForeignKey(verbose_name="团队", to="Team", on_delete=models.CASCADE)
    code = models.SlugField(verbose_name="角色代码", max_length=128, db_index=True)
    name = models.CharField(verbose_name="角色名称", max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "项目角色"
        verbose_name_plural = verbose_name
        unique_together = ("team", "code")


class ProjectUser(BaseModel):
    """
    项目成员
    """
    delete_time_field_name = "time_deleted"  # 删除的时候自动添加时间

    project = models.ForeignKey(verbose_name="项目", to="Project", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="User", on_delete=models.CASCADE)
    role = models.ForeignKey(verbose_name="项目角色", to="ProjectRole", on_delete=models.CASCADE)
    time_deleted = models.DateTimeField(verbose_name="删除事件", blank=True, null=True)

    class Meta:
        verbose_name = "项目用户"
        verbose_name_plural = verbose_name
        # unique_together = ("project", "user", "role")


class Project(BaseModel):
    """项目"""
    # 删除的时候，自动修改的字段
    delete_update_fields = ('code',)
    team = models.ForeignKey(verbose_name="团队", to="Team", on_delete=models.CASCADE)
    code = models.SlugField(verbose_name="项目代码", max_length=60)
    name = models.CharField(verbose_name="项目名称", max_length=128, blank=True, null=True)
    description = models.CharField(verbose_name="描述", max_length=512, blank=True, null=True)

    # 项目所有者
    owner = models.ForeignKey(verbose_name="所有者", to="User", related_name="project_owner",
                              blank=True, null=True, on_delete=models.CASCADE)
    # 项目成员
    users = models.ManyToManyField(verbose_name="项目成员", related_name="projects", blank=True,
                                   to="User", through=ProjectUser)
    # 状态
    is_active = models.BooleanField(verbose_name="状态", blank=True, default=True)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name
        # 团队里面项目代码是唯一的
        unique_together = ("team", "code")



