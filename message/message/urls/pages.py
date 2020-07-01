# -*- coding:utf-8 -*-
from django.urls import path

from account.views.pages.user import (
    UserLoginPageView,
    UserInfoPageView,
    UserLogoutPageView,
)

urlpatterns = [
    # 前缀：/
    path("user/login", UserLoginPageView.as_view(), name="login"),
    path("user/info", UserInfoPageView.as_view(), name="info"),
    path("user/logout", UserLogoutPageView.as_view(), name="logout"),
]
