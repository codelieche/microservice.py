# -*- coding:utf-8 -*-
"""
安全日志的url
"""
from django.urls import path

from account.views.safelog import SafeLogListApiView


urlpatterns = [
    # 前缀：/api/v1/account/safelog/
    path("list", SafeLogListApiView.as_view(), name="list"),
]
