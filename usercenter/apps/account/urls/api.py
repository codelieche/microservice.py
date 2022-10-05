# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views.test import TestView
from account.views.user import (
    LoginView,
    UserApiViewSet
)
from account.views.team import TeamApiViewSet
from account.views.system import SystemApiViewSet
from account.views.permission import PermissionApiViewSet
from account.views.role import RoleApiViewSet
from account.views.project import (
    ProjectApiViewSet, ProjectRoleApiViewSet, ProjectUserApiViewSet
)
from account.views.statis import StatisApiView

router = DefaultRouter()
router.register('user', UserApiViewSet)
router.register('team', TeamApiViewSet)
router.register('system', SystemApiViewSet)
router.register('permission', PermissionApiViewSet)
router.register('role', RoleApiViewSet)
router.register('project', ProjectApiViewSet)
router.register('projectrole', ProjectRoleApiViewSet)
router.register('projectuser', ProjectUserApiViewSet)
router.register('statis', StatisApiView)


urlpatterns = [
    # 前缀：/api/v1/account
    # 前缀: /api/v1/
    # ViewSet
    path('', include(router.urls), name="account"),

    path('login', LoginView.as_view(), name='login'),

    # test api
    path('test', TestView.as_view(), name="test"),
]
