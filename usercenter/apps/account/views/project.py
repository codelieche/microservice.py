# -*- coding:utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from codelieche.django.views.mixins import BatchActionMixin
from account.models.project import Project, ProjectRole, ProjectUser
from account.serializers.project import (
    ProjectModelSerializer,
    ProjectRoleModelSerializer,
    ProjectUserModelSerializer
)


class ProjectApiViewSet(ModelViewSet):
    """
    Project Api View Set
    """
    queryset = Project.objects.filter(deleted=False)
    serializer_class = ProjectModelSerializer
    serializer_class_set = (ProjectModelSerializer,)
    permission_classes = (IsAuthenticated,)
    # 设置根据团队id过滤
    filter_filed_name = 'team_id'

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("team__name", "code", "name")
    filterset_fields = ("team", "code", "name")
    ordering_fields = ("id", "team", "code", "name")
    ordering = ("id",)


class ProjectRoleApiViewSet(ModelViewSet):
    """
    Project Role Api View Set
    """
    queryset = ProjectRole.objects.filter(deleted=False)
    serializer_class = ProjectRoleModelSerializer
    serializer_class_set = (ProjectRoleModelSerializer,)
    permission_classes = (IsAuthenticated,)
    # 设置根据团队id过滤
    filter_filed_name = 'team_id'

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("team__name", "code", "name")
    filterset_fields = ("team", "code", "name")
    ordering_fields = ("id", "team", "code", "name")
    ordering = ("id",)

    def list(self, request, *args, **kwargs):
        # 普通用户获取列表需要指定team值
        # user = request.user
        # 普通用户是获取到自己的team，然后获取相关的数据
        return super().list(request, *args, **kwargs)


class ProjectUserApiViewSet(BatchActionMixin, ModelViewSet):
    """
    Project User Api View Set
    """
    queryset = ProjectUser.objects.filter(deleted=False)
    serializer_class = ProjectUserModelSerializer
    serializer_class_set = (ProjectUserModelSerializer,)
    permission_classes = (IsAuthenticated,)
    # 设置根据团队id过滤
    filter_filed_name = 'project__team_id'

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("project__name", "user__username", "role__name")
    filterset_fields = ("project", "user", "role")
    ordering_fields = ("id", "project", "user", "role")
    ordering = ("id",)

    # def get_serializer(self, *args, **kwargs):
    #     # 添加的时候，如果传递的是数组，那么就可以批量创建
    #     if self.action == "create" and isinstance(kwargs.get('data', {}), list):
    #         kwargs['many'] = True
    #     return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().create(request, *args, **kwargs)
