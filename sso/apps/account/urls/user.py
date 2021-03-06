# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views.user import (
    LoginView, user_logout,
    UserCreateApiView,
    UserListApiView,
    UserAllListApiView,
    UserDetailApiView,
    UserChangePasswordApiView,
    UserResetPasswordApiView
)
from account.views.token import (
    ObainRestFrameworkAuthTokenApiView,
    JwtTokenObtainPairView
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
    # JWT
    path('jwt-token', JwtTokenObtainPairView.as_view(), name="jwt-token"),
    path('jwt-token-refresh', TokenRefreshView.as_view(), name="jwt-token-refresh"),

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
