# -*- coding:utf-8 -*-
from django.urls import path

from account.views.user import (
    LoginView, user_logout,
    UserListApiView,
    UserAllListApiView,
    UserDetailApiView,
)
from account.views.token import (
    ObainRestFrameworkAuthTokenApiView
)


urlpatterns = [
    # 前缀：/api/v1/account/user/
    # 登录、退出
    path("login", LoginView.as_view(), name="login"),
    path("logout", user_logout, name="logout"),

    # token相关:
    path('api-auth-token', ObainRestFrameworkAuthTokenApiView.as_view(), name="api-auth-token"),
    path('drf-token', ObainRestFrameworkAuthTokenApiView.as_view(), name="drf-token"),
    path('token', ObainRestFrameworkAuthTokenApiView.as_view(), name="token"),
    # DRF Token使用示例： curl http://127.0.0.1:8000/api/v1/account/info --header 'Authorization:Token TOKEN_VALUE'

    # 用户相关api
    path("list", UserListApiView.as_view(), name="list"),
    path("all", UserAllListApiView.as_view(), name="all"),
    path('<int:pk>', UserDetailApiView.as_view(), name="detail"),
    path('<str:username>', UserDetailApiView.as_view(lookup_field="username"), name="detail2"),

    # 密码相关
]
