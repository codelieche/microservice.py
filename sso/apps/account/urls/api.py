# -*- coding:utf-8 -*-
from django.urls import path, include

from account.views.user import (
    LoginView, user_logout,
    UserSelfInfoApiView
)


urlpatterns = [
    # 前缀：/api/v1/account/
    path("login", LoginView.as_view(), name="login"),
    path("logout", user_logout, name="logout"),

    # user相关的api
    path('group/', include(arg=('account.urls.group', 'account'), namespace='group')),
    path("user/", include(arg=("account.urls.user", "user"), namespace="user")),
    path('info', UserSelfInfoApiView.as_view(), name="info"),
    # 权限
    path('permission/', include(arg=('account.urls.permission', 'account'), namespace="permission")),
    # 登录券
    path("ticket/", include(arg=("account.urls.ticket", "account"), namespace="ticket")),
    # 安全日志
    path("safelog/", include(arg=("account.urls.safelog", "account"), namespace="safelog")),
]
