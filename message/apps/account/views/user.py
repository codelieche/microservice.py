# -*- coding:utf-8 -*-
"""
账号登录登出相关api
"""
import re

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseForbidden

from account.models import User
from account.serializers.user import (
    UserModelSerializer,
    UserLoginSerializer,
    UserAllListSerializer,
    UserDetailSerializer,
    UserSelfDetailSerializer,
    UserChangePasswordSerializer,
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
            user = authenticate(request=request, username=username, password=password)

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
                    content = {
                        "status": False,
                        "message": "用户({})已被禁用".format(user.username)
                    }

                return JsonResponse(data=content, status=status.HTTP_200_OK)
            else:
                content = {
                    "status": False,
                    "message": "账号或者密码不正确"
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


class UserListApiView(generics.ListAPIView):
    """
    用户列表API
    """
    queryset = User.objects.all()
    serializer_class = UserAllListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("username", "mobile", "nick_name", "email")
    filter_fields = ("is_active", "is_superuser", "is_deleted", "can_view")
    ordering_fields = ("id", "can_view", "is_superuser", "is_active", "is_deleted")
    ordering = ("id",)


class UserAllListApiView(generics.ListAPIView):
    """
    所有用户列表API
    """
    queryset = User.objects.all()
    serializer_class = UserAllListSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("username", "mobile", "nick_name", "email")
    filter_fields = ("is_active", "is_superuser", "is_deleted", "can_view")
    ordering_fields = ("id", "can_view", "is_superuser", "is_active", "is_deleted")


class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    用户详情api
    1. GET：获取用户详情
    2. PUT：修改用户信息
    3. DELTE：删除用户信息【需要自定义】
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # 权限控制
    permission_classes = (DjangoModelPermissions, )

    def delete(self, request, *args, **kwargs):
        # 第1步：获取到用户
        user = self.get_object()
        if user == request.user:
            content = {
                "message": "不可删除自己"
            }
            return Response(content, status=400)

        # 第2步：对用户进行删除
        # 2-1：设置deleted和is_active
        user.is_deleted = True
        user.is_active = False
        user.save()

        # 第3步：返回响应
        response = Response(status=204)
        return response


class UserSelfInfoApiView(generics.RetrieveUpdateAPIView):
    """
    用户详情api
    1. GET：获取用户详情
    2. PUT：修改用户信息
    3. DELTE：删除用户信息【需要自定义】
    """
    queryset = User.objects.all()
    serializer_class = UserSelfDetailSerializer
    # 权限控制
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        return user
