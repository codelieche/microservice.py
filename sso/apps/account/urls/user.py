# -*- coding:utf-8 -*-
from django.urls import path

from account.views.user import (
    LoginView, user_logout,
    UserCreateApiView,
    UserListApiView,
    UserAllListApiView,
    UserDetailApiView,
    UserChangePasswordApiView,
    UserResetPasswordApiView
)


urlpatterns = [
    # 前缀：/api/v1/account/user/
    # 登录、退出
    path("login", LoginView.as_view(), name="login"),
    path("logout", user_logout, name="logout"),

    # 用户相关api
    path("create", UserCreateApiView.as_view(), name="create"),
    path("list", UserListApiView.as_view(), name="list"),
    path("all", UserAllListApiView.as_view(), name="all"),
    path('<int:pk>', UserDetailApiView.as_view(), name="detail"),
    path('<str:username>', UserDetailApiView.as_view(lookup_field="username"), name="detail2"),

    # 密码相关
    path('password/change', UserChangePasswordApiView.as_view(), name="password_change"),
    path('password/reset', UserResetPasswordApiView.as_view(), name="password_reset"),
]
