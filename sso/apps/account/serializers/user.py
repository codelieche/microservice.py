# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """
    User Model Serializer
    """

    def create(self, validated_data):
        request = self.context["request"]
        # 密码校验
        password = request.data.get("password")
        re_password = request.data.get("re_password")

        if password and re_password:
            if password != re_password:
                raise serializers.ValidationError("密码和确认密码不相同")
        else:
            raise serializers.ValidationError("请输入密码和确认密码")

        instance = super().create(validated_data=validated_data)

        # 设置密码
        instance.set_password(password.strip())
        instance.nick_name = instance.username
        # 注册的用户都需要管理员，手动设置其是否可访问本系统
        instance.can_view = False
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "username", "nick_name", "mobile", "email", "qq", "wechart", "dingding")


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录 Serializer
    """
    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)


class UserAllListSerializer(serializers.ModelSerializer):
    """
    列出所有用户的Model Serializer
    """

    class Meta:
        model = User
        fields = (
            "id", "username", "nick_name", "mobile", "email",
            "qq", "wechart", "dingding",
            "can_view", "date_joined", "is_superuser", "is_active", "last_login", "is_deleted"
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情/编辑 Model Serializer
    """

    class Meta:
        model = User

        fields = (
            "id", "username", "nick_name", "mobile", "email",
            "qq", "wechart", "dingding",
            "can_view", "date_joined", "is_superuser", "is_active", "last_login", "is_deleted"
        )
        read_only_fields = ("id", "username", "last_loogin")


class UserSelfDetailSerializer(serializers.ModelSerializer):
    """
    用户自己详情/编辑 Model Serializer
    """

    class Meta:
        model = User

        fields = (
            "id", "username", "nick_name", "mobile", "email",
            "qq", "wechart", "dingding",
            "can_view", "date_joined", "is_superuser", "is_active", "last_login", "is_deleted"
        )
        read_only_fields = ("id", "can_view", "is_active", "is_deleted", "is_superuser", "username", "last_loogin")


class UserChangePasswordSerializer(serializers.Serializer):
    """用户修改密码 Serializer"""
    username = serializers.CharField(max_length=40, required=True)
    old_password = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)
    re_password = serializers.CharField(max_length=40, required=True)
