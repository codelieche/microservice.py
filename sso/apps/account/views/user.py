# -*- coding:utf-8 -*-
"""
账号登录登出相关api
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from account.serializers.user import (
    UserLoginSerializer,
)


class LoginView(APIView):
    """
    用户登录api view
    1. GET：判断用户是否登录
    2. POST：账号登录
    """

    def get(self, request):
        # get判断当前客户端是否登录
        # 如果登录了返回{logined: true}, 未登录返回{logined: false}
        user = request.user
        if user.is_authenticated:
            content = {
                "logined": True,
                "username": user.username,
            }
        else:
            content = {
                "logined": False
            }
        return JsonResponse(data=content)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username", "")
            password = serializer.validated_data.get("password", "")

            # 调用authenticate方法：注意settings.py中的AUTHICATIOON_BACKENDS
            user = authenticate(username=username, password=password)

            if user is not None:
                # 判断用户是否可以访问本系统
                if not user.can_view:
                    content = {
                        "status": False,
                        "message": "用户({})不能访问本系统，请找管理员开通访问权限".format(user.username)
                    }
                    return JsonResponse(data=content, status=status.HTTP_403_FORBIDDEN)

                # 登录
                if user.is_active:
                    login(request, user)
                    content = {
                        "status": True,
                        "username": user.username,
                        "message": "登录成功"
                    }
                else:
                    coontent = {
                        "status": False,
                        "message": "用户({})已被禁用".format(user.username)
                    }

                return JsonResponse(data=content, status=status.HTTP_200_OK)
            else:
                # 用户不存在
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_logout(request):
    """
    退出登录
    :param request: http请求
    :return:
    """
    logout(request)
    # 有时候会传next
    next_url = request.GET.get("next", "/")
    content = {
        "status": True,
        "next": next_url
    }
    return JsonResponse(data=content)
