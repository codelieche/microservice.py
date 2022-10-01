# -*- coding:utf-8 -*-
# import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from codelieche.django.views import ModelViewSet
from account.models import User
from account.serializers.user import (
    UserLoginSerializer,
    UserModelSerializer,
    UserModelInfoSerializer
)
from account.serializers.team import TeamModelSerializer
from account.serializers.permission import PermissionModelSerializer


class LoginView(APIView):
    """
    用户登录api view
    1. GET：判断用户是否登录
    2. POST: 用户登录
    """

    def get(self, request):
        # get判断当前客户端是否登陆
        # 如果登陆了返回{logined: true},未登录返回{logined: false}
        user = request.user
        if user.is_authenticated:
            content = {
                "logined": True,
                "username": user.username,
                "nick_name": user.nick_name,
                "is_superuser": user.is_superuser,
                "user": UserModelSerializer(user).data
            }
        else:
            content = {
                "logined": False
            }

        return Response(data=content)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username", "")
            password = serializer.validated_data.get("password", "")

            user = User.objects.filter(username=username).first()

            if user is not None and user.check_password(password):
                # 判断是否可以访问本系统
                if not user.can_view:
                    content = {
                        "status": False,
                        "message": "用户({})不能访问本系统，请找管理员开通访问权限".format(user.username)
                    }
                    return Response(data=content, status=status.HTTP_403_FORBIDDEN)

                # 登陆
                if user.is_active:
                    token_seconds = 3600 * 12
                    # jwt token
                    content = {
                        "status": True,
                        "username": user.username,
                        "message": "登陆成功",
                        "token": user.generate_jwt_token(seconds=token_seconds),
                        "seconds": token_seconds,
                        "user": UserModelSerializer(user).data
                    }
                else:
                    content = {
                        "status": False,
                        "message": "用户({})已被禁用".format(user.username)
                    }
                return Response(data=content, status=status.HTTP_200_OK)
            else:
                content = {
                    "status": False,
                    "message": "账号或者密码不正确"
                }
                return Response(data=content, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApiViewSet(ModelViewSet):
    """
    User Api View Set
    """
    queryset = User.objects.filter(id__gte=0)
    serializer_class = UserModelSerializer
    serializer_class_set = (UserModelSerializer, UserModelInfoSerializer)
    permission_classes = (IsAuthenticated,)

    # filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ("username", "phone")
    # 新版本不再是filter_fields了，而是filterset_fields
    filterset_fields = ("is_active", "is_superuser", "can_view", "username")
    ordering_fields = ("id", "phone", "username")
    ordering = ("id",)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(methods=["GET"], detail=False, description="获取用户所在的团队")
    def teams(self, request):
        user = request.user
        # 获取团队列表
        teams = user.team_set.filter(deleted=False)
        serializer = TeamModelSerializer(teams, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, description="获取当前用户的所有权限")
    def permissions(self, request, pk=None):
        permissions = request.user.get_permissions()
        permissions_list = []
        for p in permissions:
            permissions_list.append(p)

        serializer = PermissionModelSerializer(permissions_list, many=True)
        return Response(data=serializer.data, status=200)

    @action(methods=["POST"], detail=False, description="校验用户的权限")
    def auth(self, request, pk=None):
        permissions = request.user.get_permissions()
        permissions_list = []
        for p in permissions:
            permissions_list.append(p)

        serializer = PermissionModelSerializer(permissions_list, many=True)
        return Response(data=serializer.data, status=200)
