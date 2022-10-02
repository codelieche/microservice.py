# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views.test import TestView
from account.views.user import (
    LoginView,
    UserApiViewSet
)
from account.views.team import TeamApiViewSet


router = DefaultRouter()
router.register('user', UserApiViewSet)
router.register('team', TeamApiViewSet)


urlpatterns = [
    # 前缀：/api/v1/account
    # 前缀: /api/v1/
    # ViewSet
    path('', include(router.urls), name="account"),

    path('login', LoginView.as_view(), name='login'),

    # test api
    path('test', TestView.as_view(), name="test"),
]
