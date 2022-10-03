# -*- coding:utf-8 -*-
from django.http.response import Http404
from django.db.models import Count, F, Sum, Avg
from rest_framework.response import Response
from rest_framework.decorators import action

from codelieche.django.views.viewset import ModelViewSet
from account.models.team import Team
from account.models.user import User
from account.models.system import System
from account.models.role import Role
from account.models.project import Project, ProjectRole
from account.serializers.user import UserModelSerializer


class StatisApiView(ModelViewSet):
    """
    用户模块统计的接口
    """
    queryset = User.objects.none()
    serializer_class = UserModelSerializer

    @action(methods=["GET"], description="统计总数的接口", detail=False)
    def count(self, request, pk=None):
        # 1. 准备统计的结果
        results = {}

        # 2. 开始统计团队相关数据
        teams = Team.objects.filter(deleted=False).\
            aggregate(team_total=Count("id"), team_active_total=Count("id", F("is_active")))
        results.update(teams)

        # 3. 用户相关统计
        users = User.objects.aggregate(user_total=Count('id'),
                                       user_active_total=Count('id', F('is_active')),
                                       user_superuser_total=Count('id', F('is_superuser')))
        results.update(users)

        # 4. 系统和角色统计
        # 4-1: 系统
        systems = System.objects.filter(deleted=False).aggregate(system_total=Count('id'))
        results.update(systems)
        # 4-2：角色
        roles = Role.objects.filter(deleted=False).aggregate(role_total=Count('id'))
        results.update(roles)

        # 5. 项目相关统计
        # 5-1: 项目
        projects = Project.objects.filter(deleted=False).aggregate(
            project_total=Count("id")
        )
        results.update(projects)
        # 5-2：项目角色
        project_roles = ProjectRole.objects.filter(deleted=False).aggregate(
            project_role_total=Count("id")
        )
        results.update(project_roles)

        # 最后：返回统计结果
        return Response(results)

    def list(self, request, *args, **kwargs):
        return Response(status=204)

    def retrieve(self, request, *args, **kwargs):
        return Http404()


