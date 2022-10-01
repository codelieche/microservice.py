# -*- coding:utf-8 -*-
from rest_framework import serializers

from account.serializers.role import RoleModelSerializer
from account.models.user import User


class UserLoginSerializer(serializers.Serializer):
    """用户登录 Serializer"""
    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=40, required=True)


class UserModelSerializer(serializers.ModelSerializer):
    """User Model Serializer"""

    def create(self, validated_data):
        request = self.context["request"]
        # 密码校验
        password = request.data.get("password")
        re_password = request.data.get("re_password")

        if password and re_password:
            if password != re_password:
                raise serializers.ValidationError("输入的密码不相同")
        else:
            raise serializers.ValidationError("请输入密码和重复密码")

        instance = super().create(validated_data=validated_data)

        # 设置密码
        instance.set_password(password.strip())
        instance.nick_name = instance.username
        # 注册的用户都需要管理员，手动设置其是否可访问本系统
        instance.can_view = False

        # 如果当前登录了用户，且是超级管理员，那么是可以设置其它字段
        user = request.user
        if user.is_superuser:
            for item in ['is_active', 'is_superuser', 'can_view']:
                value = request.data.get(item)
                if value:
                    setattr(instance, item, value)
            instance.can_view = True

        instance.save()
        return instance

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nick_name', 'email', 'phone', 'roles',
            'is_active', 'is_staff', 'is_superuser', 'can_view'
        )


class UserModelInfoSerializer(serializers.ModelSerializer):
    """User Model Info Serializer"""

    roles = RoleModelSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'nick_name', 'email', 'phone', 'roles',
            'is_active', 'is_staff', 'is_superuser', 'can_view'
        )
