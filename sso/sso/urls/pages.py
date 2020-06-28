# -*- coding:utf-8 -*-
from django.urls import path

from account.views.pages.user import (
    UserLoginPageView,
    UserLogoutPageView
)

urlpatterns = [
    # 前缀：/
    path("user/login", UserLoginPageView.as_view(), name="login"),
    path("user/logout", UserLogoutPageView.as_view(), name="logout"),
]
