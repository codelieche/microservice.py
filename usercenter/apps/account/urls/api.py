# -*- coding:utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views.test import TestView

router = DefaultRouter()

urlpatterns = [
    # 前缀：/api/v1/account
    # 前缀: /api/v1/
    # ViewSet
    path('', include(router.urls), name="account"),

    # test api
    path('test', TestView.as_view(), name="test"),
]
