# -*- coding:utf-8 -*-
from django.urls import path, include

from account.views.user import LoginView, user_logout


urlpatterns = [
    # 前缀：/api/v1/account/
    path("login", LoginView.as_view(), name="login"),
    path("logout", user_logout, name="logout"),

]
